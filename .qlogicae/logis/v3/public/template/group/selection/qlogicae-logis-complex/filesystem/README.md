</br>

<div style="width: 100%; display: flex; justify-content: center;">
    <image alt="the ${{ main-company-base-name }} logo" src="${{ main-company-base-logo-filesystem-path }}" width="256px">
</div>

</br>



<div style="text-align: center;">
  <h1>
    ${{ qlogicae-logis-display-brand-name }}
  </h1>
  <p style="font-style: italic;">
    ${{ qlogicae-logis-base-description }}
  </p>
<div style="margin: 32px 64px;">

![Project - Version](https://img.shields.io/badge/Version-${{ qlogicae-logis-current-version-label }}-blue)
[![Python - Versions](https://img.shields.io/badge/Python-3.12|%933.13|%933.14-blue?logo=python&logoColor=gold)](https://www.python.org/)
![License - MIT](https://img.shields.io/badge/License-MIT-red)

![GitHub - Stars](https://img.shields.io/github/stars/CedricDeVon/qlogicae-logis)
[![GitHub - Actions](https://github.com/CedricDeVon/qlogicae-logis/actions/workflows/quality-assurance.yml/badge.svg)](https://img.shields.io/github/actions/workflow/status/CedricDeVon/qlogicae-logis/codeql.yml)

  </div>
</div>

</br>



<h2>📚 Table of Contents</h2>
<ul>
  <li>
    <a href="#about">
      About
    </a>
  </li>
  <ul>
    <li>
      <a href="#about-description">
        Description
      </a>
    </li>
    <li>
      <a href="#about-supported-platforms">
        Supported Platforms
      </a>
    </li>
    <li>
      <a href="#about-core-features">
        Core Features
      </a>
    </li>
    <li>
      <a href="./documentation/index.md">
        Extended Documentation
      </a>
    </li>
  </ul>
  <li>
    <a href="#usage">
      Usage
    </a>
    <ul>
      <li>
        <a href="#usage-pre-requisites">
          Pre-Requisites
        </a>
      </li>
      <li>
        <a href="#usage-installation">
          Installation
        </a>
      </li>
    </ul>
  </li>
  <li>
    <a href="#development">
      Development
    </a>
    <ul>
      <li>
        <a href="#development-pre-requisites">
          Pre-Requisites
        </a>
      </li>
      <li>
        <a href="#development-setup">
          Setup
        </a>
      </li>
    </ul>
  </li>
  <li>
    <a href="#contribution">
      Contribution
    </a>
  </li>
  <li>
    <a href="#legalities">
      Legalities
    </a>
    <ul>
      <li>
        <a href="#legalities-license">
          License
        </a>
      </li>
    </ul>
  </li>  
</ul>

</br>



<h2 id="about">
  📖 About
</h2>
<h3 id="about-description">
  🧾 Description
</h3>
<p style="font-style:italic">
  "With a lack of hardware, why not optimize your workflow?"
</p>
<p>
  <strong>QLogicae Logis</strong> is an opinionated, multi-platform, multi-project, software development tool, as a CLI, written in Python3.
</p>
<ul>
  <li>
    <p>
      <strong>Opinionated</strong> - For software development contributions, regardless of programming language and integrated tools of choice.
    </p>
  </li>
  <li>
    <p>
      <strong>Multi-platform</strong> - Maximizing usability, to develop software projects, across multiple operating systems.
    </p>
  </li>
  <li>
    <p>
      <strong>Software Automation</strong> - Implemented via user-defined CI/CD-like workflow YAML files. Notable major operations include: workflow macros programming, and filesystem template application across multiple projects.
    </p>
  </li> 
  <li>
    <p>
      <strong>Python3</strong> - The main project programming language of choice, with the aim to ease development time, learning curve, ease of collaboration, and multi-platform usage stability. Having said that, if it works, it works - that's what matters.
    </p>
  </li>
</ul>

<p>
  <strong>ADVICE</strong>: To get things straight, this tool is best suited for orchestrating multiple projects with a shared deliverable. Developers can still utilize its features for relatively small, single-repository projects. Having said that, please do review your own project requirements.
</p>



<h3 id="about-core-features">
  ⚙️ Core Features
</h3>
<p>
  More can be added, eventually. What this project offers now to its users (and contributors) are as follows:
</p>
<ul>
  <li>
    <p>
      CI/CD Workflow Implementations via YAML Files
    </p>
  </li>
  <li>
    <p>
      Filesystem Templates
    </p>
  </li>
  <li>
    <p>
      Workflow Macros Programming
    </p>
  </li>
  <li>
    <p>
      3rd-Party Plugin API
    </p>
  </li>
  <li>
    <p>
      And more to come!
    </p>
  </li>
</ul>

</br>

<p>
  To know more, check out the <a href="./documentation/index.md">extended documentation</a>.
</p>

</br>



<h2 id="usage">
  🧑‍💻 Usage
</h2>

<h3 id="usage-prerequisites">
  📋 Prerequisites
</h3>

<p>
  For maximum convenience, please make sure these minimum system requirement(s) are met and have installed the following software:
</p>

<ul>
  <li>
    <p>
      <strong>Python Runtime</strong> >= 3.12
    </p>
  </li>
  <li>
    <p>
      <strong>Disk Memory Storage</strong> < 1 MB
    </p>
  </li>
  <li>
    <p>
      <strong>Supported Platform(s)</strong>    
      <ul>
        <li>
          <p>Windows 11</p>
        </li>
        <li>
          <p>macOS</p>
        </li>
        <li>
          <p>Linux Ubuntu</p>
        </li>
      </ul>
    </p>
  </li>
</ul>

<h3 id="usage-installation">
  🛠️ Installation
</h3>

<p>
  This tool can be installed as a Python PIP package, either globally or within virtual environments.
</p>
<ol>
  <li>
    <p>
      First, simply copy and paste the
      <code>pip install qlogicae-logis</code>
      command into your command-line interface of choice. If you intend to
      use a Python virtual environment, activate your environment first,
      then run the installation command.
    </p>
  </li>

  <li>
    <p>
      After the installation completes, run
      <code>qlogicae-logis about version</code>.
      An error-free display showing the application version should confirm
      a successful installation, at minimum.
    </p>
  </li>
</ol>

</br>



<h2 id="development">
  🏗️ Development
</h2>

<h3 id="development-prerequisites">
  📋 Prerequisites
</h3>

<p>
  For maximum convenience, please make sure these minimum system requirement(s) are met and have installed the following software:
</p>

<ul>
  <li>
    <p>
      <strong>.pyenv file</strong> (Please send a request via email)
      <ul>
        <li>
          <p></p>
        </li>
      </ul>
    </p>
  </li>
  <li>
    <p>
      <strong>Python Runtime</strong> >= 3.12
    </p>
  </li>
  <li>
    <p>
      <strong>Supported Platform(s)</strong>    
      <ul>
        <li>
          <p>Windows 11</p>
        </li>
        <li>
          <p>macOS</p>
        </li>
        <li>
          <p>Linux Ubuntu</p>
        </li>
      </ul>
    </p>
  </li>
</ul>

<h3 id="development-setup">
  🛠️ Setup
</h3>

<p>
  You can begin developing and contributing on this project by following these recommended instructions first:
</p>

<ol>
  <li>
    <p>Fork this repository.</p>
  </li>
  <li>
    <p>Clone your forked repository to a filesystem path of your choosing.</p>
  </li>
  <li>
    <p>Open a console of your choosing and navigate to your forked project folder.</p>
  </li>
  <li>
    <p>Create a virtual environment via <code>python3 -m venv .venv</code>.</p>
  </li>
  <li>
    <p>
      Activate your virtual environment, depending on your currently running
      operating system, via one of the following:
    </p>
    <ul>
      <li>
        <p><strong>Linux</strong>: <code>source .venv/bin/activate</code></p>
      </li>
      <li>
        <p><strong>MacOS</strong>: <code>.venv\Scripts\activate.bat</code></p>
      </li>
      <li>
        <p><strong>Windows</strong>: <code>.venv\Scripts\Activate.ps1</code></p>
      </li>
    </ul>
  </li>
  <li>
    <p>
      Install all development dependencies found within 'project.optional-dependencies' within the <a href="pyproject.toml">pyproject.toml</a> file.
    </p>    
  </li>
</ol>

</br>



<h2 id="contribution">
  🤝 Contribution
</h2>

<p>
  Meaningful contributions always welcome! Having said that, please be guided with the following documentation based on what aspects of the project you want to be improved upon.
</p>

<ul>
  <li>
    <p><a href="./CONTRIBUTING.md">Contribution Guidelines</a></p>
  </li>
  <li>
    <p><a href="./SECURITY.md">Security Guidelines</a></p>
  </li>
  <li>
    <p><a href="./.github/ISSUE_TEMPLATE/bug_report.md">Bug Reports</a></p>
  </li>
  <li>
    <p><a href="./.github/ISSUE_TEMPLATE/feature_request.md">Feature Requests</a></p>
  </li>
  <li>
    <p><a href="./.github/PULL_REQUEST_TEMPLATE.md">Pull Requests</a></p>
  </li>
</ul>

</br>



<h2 id="legalities">
  🏛️ Legalities
</h2>

<h3 id="legalities-license">
  📋 License
</h3>

<p>
  The project is currently under the <a href="./LICENSE">MIT License</a>.
</p>

</br>
