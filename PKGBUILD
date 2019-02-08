# Maintainer: Eric Torres <erictorres4@protonmail.com>
pkgname=rbackup
pkgver=0
pkgrel=1
pkgdesc="An rsync-based tool for backing up files"
arch=('any')
url=""
license=('MIT')
groups=()
depends=('python')
makedepends=('git' 'python-setuptools')
checkdepends=('python-pytest')
backup=()
source=("file:///${HOME}/Projects/rbackup")
noextract=()

pkgver() {
	cd "$srcdir/${pkgname%-git}"
	printf "%s" "$(git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g')"

}

build() {
	cd "$srcdir/${pkgname}"
    python setup.py build
}

package() {
	cd "$srcdir/${pkgname%-git}"

    # install main package
    python setup.py install --prefix='/usr' --root="${pkgdir}" --optimize=1 --skip-build
}
