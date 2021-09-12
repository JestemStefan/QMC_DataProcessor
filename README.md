[![Total alerts](https://img.shields.io/lgtm/alerts/g/JestemStefan/QMC_DataProcessor.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JestemStefan/QMC_DataProcessor/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/JestemStefan/QMC_DataProcessor.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/JestemStefan/QMC_DataProcessor/context:python)


# QMC Data Processor

QMC Data Processor is a software to process and visualize data from Guassian structure modeling software.



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![obraz](https://user-images.githubusercontent.com/37214990/133004340-a9eb3748-da36-49e9-8771-8f5ae8c29e8f.png)                             ![obraz](https://user-images.githubusercontent.com/37214990/133004346-131518fc-c95e-4639-aab9-307dcfa96c21.png) 

This software provide a fast and easy way to process data from quantum-mechanical calculation.

Main features:
* Analysis of HF and DFT conformer search calculations with detection of duplicates and low energy conformers.
* Analysis of TD-DFT calculation of UV and ECD spectra.
* Exporting data to spreadsheat file format.

### Built With

* [Python](https://www.python.org/)
* and love to science ❤️



<!-- GETTING STARTED -->
## Getting Started

Run project using:
```sh
/qmc_dataprocessor/qmc_dataprocessor.py
```

or download dist folder from [Here](https://github.com/JestemStefan/QMC_DataProcessor/tree/main/dist) and use binary file.


<!-- USAGE EXAMPLES -->
## Usage

1. Prepare folder containing `.out` files. Files can be mixed with other formats. Correct files will be picked automagically.

![obraz](https://user-images.githubusercontent.com/37214990/133004667-4264fd42-7e12-47fd-8c41-00a40d9395a6.png)

2. Run a project or binary file. [See Getting Started]
3. Click "Select Folder" button and select folder with a files to analyze.

![obraz](https://user-images.githubusercontent.com/37214990/133004740-53988c20-84e0-4dd7-90e3-8efce599208b.png)

4. Select parameters for the analysis by entering values in entry boxes.
5. Click `Confomers energy analysis` button

After successful analysis folder with results will be automatically opened.

![obraz](https://user-images.githubusercontent.com/37214990/133004885-97580e92-60a6-4f09-a34b-5a68d96a1a7a.png)




<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/JestemStefan/QMC_DataProcessor/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the AGPL-3.0 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Bartosz Stasiak - [bs.stasiak.bartosz@gmail.com](mailto:bs.stasiak.bartosz@gmail.com)

Project Link: [https://github.com/JestemStefan/QMC_DataProcessor](https://github.com/JestemStefan/QMC_DataProcessor)
