</br>

<div style="width: 100%; display: flex; justify-content: center;">
    <image alt="${{ current-company-base-name }} logo" src="${{ current-company-base-logo-filesystem-path }}" width="256px">
</div>

</br>


<div style="text-align: center;">
  <h1>${{ current-project-display-name }}</h1>
  <p style="font-style: italic;">${{ current-project-description }}</p>
  <div style="margin: 32px 64px;">

<!-- Static Markdown Badges -->
![Project - Version](https://img.shields.io/badge/Version-${{ current-project-version-tag }}-blue)
![License - Name](https://img.shields.io/badge/License-${{ current-project-license-name }}-red)

<!-- Dynamic Markdown Badges -->
![GitHub - Stars](https://img.shields.io/github/stars/${{ current-git-username }}/${{ current-project-source-name }})
[![GitHub - Actions](https://github.com/${{ current-git-username }}/${{ current-project-source-name }}/actions/workflows/codeql.yml/badge.svg)](https://img.shields.io/github/actions/workflow/status/${{ current-git-username }}/${{ current-project-source-name }}/codeql.yml)

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
            <a href="#about-core-features">
                Core Features
            </a>
        </li>
        <li>
            <a href="${{ current-project-repository-link }}">
                Project Repository
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
				<a href="#usage-release">
					Release
				</a>
			</li>
		</ul>
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
  	[insert quote]
</p>
<p>
  	[...]
</p>
<h3 id="about-core-features">
  	⚙️ Core Features
</h3>
<p>
  	More can be added, eventually. What this project offers now is as follows:
</p>
<ul>
	<li>
		<p>
			[...]
		</p>
	</li>
</ul>

</br>

<p>
  	For more information, please visit the <a href="${{ current-project-repository-link }}">Project Repository</a>.
</p>

</br>



<h2 id="usage">
  	🧑‍💻 Usage
</h2>
<h3 id="usage-pre-requisites">
  	📋 Prerequisites
</h3>
<p>
  	For maximum convenience, please re-evaluate your system if these requirements are met:
</p>
<h4>
  	🔻 Minimum
</h4>
<ul>
	<li>
		<p>
		[...]
		</p>
	</li> 
</ul>

<h3 id="usage-release">
  	🚀 Release
</h3>

<p>
  	To get started, please follow these instructions.
</p>
<p>
  	[...]
</p>
</br>



<h2 id="legalities">
  	🏛️ Legalities
</h2>

<h3 id="legalities-license">
  	📋 License
</h3>

<p>
  	The project is currently under the <a href="./LICENSE">${{ current-project-license-name }} License</a>.
</p>

</br>
