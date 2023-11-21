#!/usr/bin/expect -f
# shellcheck disable=SC2121
set timeout 1800
set cmd [lindex "$argv" 0]
set licenses [lindex $argv 1]

spawn {*}$cmd
expect {
  "(y/N)" {
        exp_send "y\r"
        exp_continue
  }
  eof
}
