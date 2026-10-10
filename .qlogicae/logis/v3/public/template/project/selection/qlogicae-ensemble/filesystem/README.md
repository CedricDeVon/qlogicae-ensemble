</br>
<div style="width: 100%; display: flex; justify-content: center;">
    <image alt="${{ main-company-display-name }} logo" src="${{ main-company-base-logo-filesystem-path }}" width="256px">
</div>
</br>



<div style="text-align: center;">
  <h1>${{ qlogicae-ensemble-brand-display-name }}</h1>
  <p style="font-style: italic;">${{ qlogicae-ensemble-project-base-description }}</p>
  <div style="margin: 32px 64px;">

<!-- Static Markdown Badges -->
![Project - Version](https://img.shields.io/badge/Version-${{ qlogicae-ensemble-version-current-label }}-blue)
![License - Name](https://img.shields.io/badge/License-${{ qlogicae-ensemble-license-display-name }}-red)

<!-- Dynamic Markdown Badges -->
![GitHub - Stars](https://img.shields.io/github/stars/${{ main-author-base-username }}/${{ qlogicae-ensemble-brand-base-name }})
[![GitHub - Actions](https://github.com/${{ main-author-base-username }}/${{ qlogicae-ensemble-brand-base-name }}/actions/workflows/codeql.yml/badge.svg)](https://img.shields.io/github/actions/workflow/status/${{ main-author-base-username }}/${{ qlogicae-ensemble-brand-base-name }}/codeql.yml)

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
            <a href="${{ qlogicae-ensemble-repository-link }}">
                Project Repository
            </a>
        </li>
    </ul>
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
  	Better safe than sorry
</p>
<p>
  	Centralized storage space. The idea of designating an area to house 'QLogicae' related resources (assets, templates, etc.) was what brought to its creation. The solution being to provide a systematic and centralized storage system: pool resources, and modify said resources in one place. These resources would mostly be trusted by the team into completing separate projects, due to previous use from legacy projects - such is the case for vendored packages.
</p>
<p>
  	Another concern involves the accidental deletion of projects, whether through human error or a buggy implementation inside the automation script. To be more specific, this repository also serves to store the base '.qlogicae' folder. Separate projects would 'synchronize', that is, in this context, to copy the '.qlogicae' folder and paste it inside this repository. This makes sense, since 'qlogicae-logis' only requires one source of truth - found at the base of the master workspace.
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
      <a href="${{ qlogicae-ensemble-design-system-link }}">
        <strong>Figma</strong>
      </a> - UI/UX design system, amongst others.
    </p>
	</li>
  <li>
		<p>
      <strong>Content Storage</strong> - Common icons, logos, templates, etc.
    </p>
	</li>
  <li>
		<p>
      <strong>Configuration Storage</strong> - Main 'QLogicae' configurations, plugins, templates, macros, etc.
    </p>
	</li>
  <li>
		<p>
      <strong>Vendored Packages</strong> - Across multiple programming languages from various package managers.
    </p>
	</li>
</ul>

</br>

<p>
  	For more information, please visit the <a href="${{ qlogicae-ensemble-repository-link }}">Project Repository</a>.
</p>

</br>



<h2 id="legalities">
  	🏛️ Legalities
</h2>

<h3 id="legalities-license">
  	📋 License
</h3>

<p>
  	The project is currently under the <a href="./LICENSE">${{ qlogicae-ensemble-license-display-name }} License</a>.
</p>

</br>
