[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Quimzy/qPeer">
    <img src="https://github.com/Quimzy/qPeer/blob/master/Logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">qPeer Protocol</h3>

  <p align="center">
    Peer-to-peer routing protocol for decentralized networks
    <br />
    <a href="https://github.com/Quimzy/qPeer"><strong>Explore the repository »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Quimzy/qPeer">View Code</a>
    ·
    <a href="https://github.com/Quimzy/qPeer/issues">Report Bug</a>
    ·
    <a href="https://github.com/Quimzy/qPeer/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#support">Support</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#benchmarks">Benchmarks</a></li>
    <li><a href="#faq">FAQ</a></li>
    <li><a href="#todo">TODO</a></li>
    <li><a href="#scripts">Scripts</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<b>qPeer</b> is a peer-to-peer routing protocol intended for running your decentralized networks.
It is the first open-source project in a series of decentralized projects under the name Quirk.

*<b>Disclaimer</b>: The project is still in experimental stage.*

### Support

* Donate to my Bitcoin Wallet: bc1qsrgawhx3g639y9pep7yqa84s26zrtrwwfcx9gd
* Donate to my Ethereum Wallet: 0xCaf0726d4eFE5291e23f9351553Cfd2DB1Af7A48


## Usage
1. Install requirements (`pip install -r requirements.txt`)
2. Change role to 1, for bootstrap peers in utils.py (line 51) 
3. Launch bootstrap.py on your bootstrap node
4. Set bootstrap peerip in main.py (line 56)
5. Launch main.py on your nodes

## Benchmarks
* Peers don't generate their peerid randomly. The peerid is based on the peer's public key.
* qPeer uses hard-coded peers just for the first connection. For future connections, it uses the other peers it found.
* qPeer stores peers information securely using cryptographic techniques
* qPeer's messages are secured with RSA & AES

## FAQ
<b>Q: qPeer is stuck/hangs/crashes.</b>

A: It takes a while (up to 1mn on older CPUs) but if you're sure it's stuck, restart qPeer.

<b>Q: qPeer shows errors like "access denied", "unable to read file", "system error"...</b>

A: Run qPeer as root.

<b>Q: My antivirus reports qPeer as malware.</b>

A: AVs seem to like it more for some reason. I suspect this occurs because of the nature and relative obscurity of qPeer (network requests/protocols...)

<b>Q: I don't like what qPeer did to my computer. How do I change it back?</b>

A: qPeer won't change any of your settings.

<b>Q: qPeer doesn't accept Internet connections</b>

A: So far, qPeer does not support Internet connections behind NAT. Although, you can enable qPeer's port manually from your router's settings.  

<!-- ROADMAP -->
## TODO
* Identifying message types and handling them based on type: Tuples *(<b>Solved</b>)*
* Accepting incoming/outcoming requests behind NAT: UPnP, Hole Punching, RTC, Quic... (<b>*Urgent*</b>)
* Improving logging for debugging purposes (<b>*Urgent*</b>)
* Implementing AI for smarter peer discovery (*Normal*)
* Enabling qPeer to work without internet connection (*Advanced*)
* Enabling peer discovery without any bootstrap peers (*Advanced*)

## Scripts
* <b>qpeer/utils.py</b>: Contains utilities required by other scripts

* <b>qpeer/errors.py</b>: Handles all exceptions

* <b>qpeer/node.py</b>: Peer discovery protocol

* <b>main.py</b>: Runs the server/client on a node

* <b>bootstrap.py</b>: Runs the server on a supernode

* <b>requirements.txt</b>: Contains all required libraries

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GNU General Public License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

**Ilyes Arfaoui** (Project Maintainer) - [@Quimzy01](https://twitter.com/Quimzy01)

**Jihed Kdiss** (Designer & Documentation Maintainer) - [@thisisjihedkdiss](https://facebook.com/thisisjihedkdiss)

Project Link: [https://github.com/Quimzy/qPeer](https://github.com/Quimzy/qPeer)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Quimzy/qPeer.svg?style=for-the-badge
[contributors-url]: https://github.com/Quimzy/qPeer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Quimzy/qPeer.svg?style=for-the-badge
[forks-url]: https://github.com/Quimzy/qPeer/network/members
[stars-shield]: https://img.shields.io/github/stars/Quimzy/qPeer.svg?style=for-the-badge
[stars-url]: https://github.com/Quimzy/qPeer/stargazers
[issues-shield]: https://img.shields.io/github/issues/Quimzy/qPeer.svg?style=for-the-badge
[issues-url]: https://github.com/Quimzy/qPeer/issues
[license-shield]: https://img.shields.io/github/license/Quimzy/qPeer.svg?style=for-the-badge
[license-url]: https://github.com/Quimzy/qPeer/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/ilyes-arfaoui-1254591a0/
