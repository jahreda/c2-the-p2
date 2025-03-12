# PHYS 790 - Day 1 - Write and Read ROOT scripts
Here we're going to look at performance statistics of writing vectors with some kinds of quantities and saving them to ROOT files. 

First you'll need to log into the UChicago AF, navigate to a work directory and 
```
### clone and navigte into to the directory
git clone https://github.com/jahreda/c2-the-p2.git
cd c2-the-p2/IO

### setup 
lsetup 'asetup main, latest, Athena'
```

Then when you want to run the `writeROOTFile.cpp` script, to do so you'll need to compile the code wile including necessary ROOT libraries: 
```
g++ -o writeROOTFile writeROOTFile.cpp `root-config --cflags --glibs`
```
and if everything compiles correctly, you should be able to 
```
./writeROOTFile
```
If you run with `N = 1e8`, then this will run for quite a while, so I recommend something running this all in a `tmux` session so if you need to leave you can return to it from a fresh terminal:
```
$ ssh user@login.af.uchicago.edu
$ tmux a
```
where `tmux a` allows you to reopen your latest tmux session.

### A word about `tmux`
`tmux` is a really useful tool for this project, because there's some serious package navigation that will leave you tired of changing directories. The way I have it setup is by creating new windows in `tmux` by doing `<Ctrl-b> + c`, renaming the window (i.e. `/python/`, `/src/`, `/build/`, etc.) with `<Ctrl-b> + ,`, and switching between windows with `<Ctrl-b> + #` where `#` is the number window you (hopefully) rename. My favorite `tmux` cheatsheet site is [here](https://tmuxcheatsheet.com/)

