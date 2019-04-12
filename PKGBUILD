# Maintainer: Eric Torres <erictorres4@protonmail.com>
pkgname=rbackup
pkgver=0.1.1
pkgrel=1
pkgdesc="An rsync-based tool for backing up files"
arch=('any')
url=""
license=('MIT')
depends=(python rsync)
makedepends=(python-setuptools)
checkdepends=(python-hypothesis python-pytest)
backup=(etc/$pkgname/backup.conf
        etc/$pkgname/include-paths.conf
        etc/$pkgname/home-exclude.conf)
source=("${pkgname}-${pkgver}.tar.gz")
sha512sums=('d46504da5c996f041f276b6045d904b9e6b5dfd18781ae7d7d308175ded1b48851c588db42752f539ab412e77a46f5e53c4d0ca08ea3545073bd1a0fce15882b')

build() {
	cd "${srcdir}/${pkgname}-${pkgver}"
    python setup.py build
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
    for config in rbackup/config/*.conf; do
        install -Dm644 "${config}" "${pkgdir}/etc/${pkgname}/${config##*/}"
    done

    # Install AppArmor profile
    install -Dm644 rbackup/config/usr.bin.backup \
        "${pkgdir}/etc/apparmor.d/usr.bin.backup"

    # Install documetation
    install -Dm644 README \
        "${pkgdir}/usr/share/doc/${pkgname}/README"
}
