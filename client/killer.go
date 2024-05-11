package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"syscall"
)

func killLS() {
	pid := locatePortPID(37722)
	if pid != 0 {
		if debug {
			fmt.Println("[killer] Attempting to kill port 37722")
		}
		err := syscall.Kill(pid, syscall.SIGKILL)
		if err != nil {
			if debug {
				fmt.Println("[killer] Failed to kill port 37722: " + err.Error())
			}
			return
		}
		if debug {
			fmt.Println("[killer] Successfully killed port 37722")
		}
	}
}

func locatePortPID(port int) int {
	tcpFile, err := os.Open("/proc/net/tcp")
	if err != nil {
		if debug {
			fmt.Println("[killer] Error opening /proc/net/tcp")
		}
		return 0
	}
	defer tcpFile.Close()

	procDir, err := os.Open("/proc") // for later use
	if err != nil {
		if debug {
			fmt.Println("[killer] Error opening /proc")
		}
		return 0
	}
	defer procDir.Close()

	scanner := bufio.NewScanner(tcpFile)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)
		// if less than 10, not a valid entry
		if len(parts) < 10 {
			continue // skip line
		}

		localAddr := parts[1]
		localPortHex := localAddr[strings.LastIndex(localAddr, ":")+1:]
		localPort, err := strconv.ParseInt(localPortHex, 16, 64) // convert port hex to integer
		if err != nil {
			continue
		}

		// check if line matches the port
		if int(localPort) == port {
			inode := parts[9]

			// iterate through each process directory
			pidDirs, err := procDir.Readdirnames(0)
			if err != nil {
				continue
			}

			for _, pidDir := range pidDirs {
				// check if the directory name is a PID
				if _, err := strconv.Atoi(pidDir); err != nil {
					continue
				}

				fdDirPath := fmt.Sprintf("/proc/%s/fd", pidDir)
				fdDir, err := os.Open(fdDirPath)
				if err != nil {
					continue
				}
				defer fdDir.Close()

				// Iterate through each file to find processes using the port's inode
				fds, err := fdDir.Readdirnames(0)
				if err != nil {
					continue
				}
				for _, fd := range fds {
					fdLink, err := os.Readlink(fmt.Sprintf("%s/%s", fdDirPath, fd))
					if err != nil {
						continue
					}

					if strings.Contains(fdLink, "socket:["+inode+"]") {
						pid, _ := strconv.Atoi(pidDir)
						return pid // Process using the port's inode found, return its PID
					}
				}
			}
		}
	}
	if debug {
		msg := fmt.Sprintf("[killer] No process found using port %d", port)
		fmt.Println(msg)
	}
	return 0 // Failed to find process using the port
}
