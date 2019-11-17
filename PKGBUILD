# Maintainer: Eric Torres <erictorres4@protonmail.com>
pkgname=rbackup
pkgver=0.7.2
pkgrel=2
pkgdesc="An rsync-based tool for backing up files"
arch=('any')
url="https://github.com/etorres4/rbackup"
license=('MIT')
depends=(python rsync)
makedepends=(python-sphinx python-setuptools)
checkdepends=(python-hypothesis python-pytest)
backup=(etc/$pkgname/backup.conf
        etc/$pkgname/backupd.conf
        etc/$pkgname/etc-include.conf
        etc/$pkgname/system-include.conf
        etc/$pkgname/home-exclude.conf)
source=("${pkgname}-${pkgver}.tar.gz")
sha512sums=('cc3bdd39b4470a53e12ef195beaa98fd7754620c5647bbdf46758d30607276095a51616d1aad4a9f653b814b41ec29253aefa7d944060971ec21feba7be56a1c')

build() {
	cd "${srcdir}/${pkgname}-${pkgver}"
    python setup.py build

    #python setup.py build_sphinx -b man
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
    install -Dm644 README.rst \
        "${pkgdir}/usr/share/doc/${pkgname}/README.rst"
}
