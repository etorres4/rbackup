# Maintainer: Eric Torres <erictorres4@protonmail.com>
pkgname=rbackup
pkgver=0.5.2
pkgrel=1
pkgdesc="An rsync-based tool for backing up files"
arch=('any')
url="https://github.com/etorres4/rbackup"
license=('MIT')
depends=(python rsync)
makedepends=(python-sphinx python-setuptools)
checkdepends=(python-hypothesis python-pytest)
backup=(etc/$pkgname/backup.conf
        etc/$pkgname/etc-include.conf
        etc/$pkgname/system-include.conf
        etc/$pkgname/home-exclude.conf)
source=("${pkgname}-${pkgver}.tar.gz")
sha512sums=('4d389c1669b54f8da3567420d786de065c81c732263068e3ac79f8dab539cf13a355fd9b54a684df30499fd760ff44be20cafc285a8d3e3fd24d367dcbd203c4')

build() {
	cd "${srcdir}/${pkgname}-${pkgver}"
    python setup.py build

    python setup.py sphinx_build
}

check() {
    cd "${srcdir}/${pkgname}-${pkgver}"
    pytest
}

package() {
	cd "${srcdir}/${pkgname}-${pkgver}"

    python setup.py install \
        --prefix='/usr' \
        --root="${pkgdir}" \
        --optimize=1 \
        --skip-build

    # Install config files
    for config in config_files/*.conf; do
        install -Dm644 "${config}" "${pkgdir}/etc/${pkgname}/${config##*/}"
    done

    # Install AppArmor profile
    install -Dm644 config_files/usr.bin.backup \
        "${pkgdir}/etc/apparmor.d/usr.bin.backup"

    # Install documetation
    install -Dm644 README \
        "${pkgdir}/usr/share/doc/${pkgname}/README"
}
