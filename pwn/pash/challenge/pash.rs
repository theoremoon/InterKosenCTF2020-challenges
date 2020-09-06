use std::collections::HashMap;
use std::io::{self, Write};
use std::process::Command;

fn cmd_whoami(_args: &mut std::str::SplitWhitespace) {
    let mut child = Command::new("whoami")
        .spawn()
        .expect("Failed to execute process");
    child.wait().expect("Failed to wait on child");
}
fn cmd_ls(_args: &mut std::str::SplitWhitespace) {
    let mut child = Command::new("ls")
        .arg("-lha")
        .spawn()
        .expect("Failed to execute process");
    child.wait().expect("Failed to wait on child");
}
fn cmd_pwd(_args: &mut std::str::SplitWhitespace) {
    let mut child = Command::new("pwd")
        .spawn()
        .expect("Failed to execute process");
    child.wait().expect("Failed to wait on child");
}
fn cmd_cat(args: &mut std::str::SplitWhitespace) {
    let path;
    match args.next() {
        None => path = "-",
        Some(arg) => path = arg
    }
    if path.contains("flag.txt") {
        println!("ฅ^•ﻌ•^ฅ < RESTRICTED!");
        return;
    }
    let mut child = Command::new("cat")
        .arg(path)
        .spawn()
        .expect("Failed to execute process");
    child.wait().expect("Failed to wait on child");
}
fn cmd_exit(_args: &mut std::str::SplitWhitespace) {
    std::process::exit(0);
}

fn main() {
    let mut f = HashMap::<String, &dyn Fn(&mut std::str::SplitWhitespace)->()>::new();
    /* set available commands */
    f.insert("whoami".to_string(), &cmd_whoami);
    f.insert("ls".to_string(), &cmd_ls);
    f.insert("pwd".to_string(), &cmd_pwd);
    f.insert("cat".to_string(), &cmd_cat);
    f.insert("exit".to_string(), &cmd_exit);

    println!("***** PASH - Partial Admin SHell *****");
    println!("  __      _  ,---------------------.  ");
    println!("o'')}}____// <' Only few commands   |  ");
    println!(" `_/      )  |      are available. |  ");
    println!(" (_(_/-(_/   '---------------------'  \n");

    loop {
        /* read input */
        print!("(admin)$ ");
        io::stdout().flush().unwrap();
        let mut s = String::new();
        io::stdin().read_line(&mut s).ok();

        /* execute command */
        let mut args = s.trim().split_whitespace();
        let cmd = args.next().unwrap();
        if f.contains_key(cmd) {
            (f.get(cmd).unwrap() as &dyn Fn(&mut std::str::SplitWhitespace)->())(&mut args);
        } else {
            println!("No such command: {}", cmd);
        }
    }
}
