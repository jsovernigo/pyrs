<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** jsovernigo, pyrs, twitter_handle, juliansovernigo@gmail.com
-->

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">PYRS</h3>

  <p align="center">
    For when you just don't have Netcat.
    ·
    <a href="https://github.com/jsovernigo/pyrs/issues">Report Bug</a>
    ·
    <a href="https://github.com/jsovernigo/pyrs/issues">Request Feature</a>
  </p>
</p>



<!-- ABOUT THE PROJECT -->
## About The Project

Pyrs is a python3 built simple reverse shell that automates Phineas Fisher's python-bash+stty raw
dumb terminal upgrade method. It is basically a wrapper around a `stty raw -echo` call to reconfigure
a terminal to accept and send control sequences over a 'dumb' pseudo-tty connection. It is by no means
complete, but makes for a nicer backdoor shell when you finally get that foothold onto the target.



### Built With
Built with Python3



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.
1. clone or download this repository
2. set the executable flag on the file (i.e. chmod +x rs.py) and run the file, OR
3. run the file with python3 ./rs.py ...

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python: https://www.python.org/downloads/

### Installation

1. Clone the repo
```sh
git clone https://github.com/jsovernigo/pyrs.git
```
thats it.


<!-- USAGE EXAMPLES -->
## Usage

Listen for an incoming connection from a reverse shell, and attempt to initialize "smart" mode
`./rs.py --smart 4444`

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/jsovernigo/pyrs/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

This project is only as good as the people using and contributing to it. Notice a bug? Open an Issue. Fix a bug? Submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/jsovernigo/pyrs](https://github.com/jsovernigo/pyrs)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

Thank you to Phineas Fisher for discovering the python pty + stty raw methods. These are essential to the
"smart" settings on the shell.

