from distutils.core import setup

setup(
  name = 'discord_interactive',         # How you named your package folder (MyLib)
  packages = ['discord_interactive'],   # Chose the same as "name"
  version = '1.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package allowing you to display interactive help in Discord easily',   # Give a short description about your library
  author = 'Nicolas REMOND',                   # Type in your name
  author_email = 'remondnicola@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/astariul/discord_interactive_help',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/astariul/discord_interactive_help/archive/v1.0.3.tar.gz',    # I explain this later on
  keywords = ['Discord', 'Interactive', 'Help'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)