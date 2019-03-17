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
        etc/$pkgname/home-exclude.conf)
source=("${pkgname}-${pkgver}.tar.gz")
sha512sums=('SKIP')

build() {
	cd "${srcdir}/${pkgname}-${pkgver}"
    python setup.py build
}

check() {
    cd "${srcdir}/${pkgname}-${pkgver}"
    python -m unittest
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"

    python setup.py install \
        --prefix='/usr' \
        --root="${pkgdir}" \
        --optimize=1 \
        --skip-build

    # Install config files
    for config in rbackup/config/*.conf; do
        install -Dm644 "${config}" "${pkgdir}/etc/${pkgname}/${config##*/}"
    done

    # Install AppArmor profile
    install -Dm644 rbackup/config/usr.bin.backup \
        "${pkgdir}/etc/apparmor.d/usr.bin.backup"

    # Install documetation
    install -Dm644 README.rst \
        "${pkgdir}/usr/share/doc/${pkgname}/README.rst"
}
