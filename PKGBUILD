# Maintainer: Eric Torres <erictorres4@protonmail.com>
pkgname=rbackup
pkgver=0.1
pkgrel=1
pkgdesc="An rsync-based tool for backing up files"
arch=('any')
url=""
license=('MIT')
depends=(python rsync)
makedepends=('git' 'python-setuptools')
checkdepends=('python-pytest')
backup=(etc/$pkgname/backup.conf
        etc/$pkgname/etc-include.conf
        etc/$pkgname/home-include.conf)
source=("file:///${HOME}/Projects/rbackup")

build() {
	cd "$srcdir/${pkgname}"
    python setup.py build
}

package() {
	cd "$srcdir/${pkgname}"

    python setup.py install \
        --prefix='/usr' \
        --root="${pkgdir}" \
        --optimize=1 \
        --skip-build

    # Install config files
    for config in rbackup/config/*; do
        install -Dm644 "${config}" "${pkgdir}/etc/${pkgname}/${config##*/}"
    done

    # Install AppArmor profile
    install -Dm644 rbackup/config/usr.bin.backup \
        "${pkgdir}/etc/apparmor.d/usr.bin.backup"
}
