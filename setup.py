from setuptools import setup
import versioneer

setup(
    name="nice_crosstab",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=["nice_crosstab"],
    install_requires=["numpy", "pandas"],
)
