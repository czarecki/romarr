"""PlayStation 4 packages can travel from a completed download to the library."""

from romarr.library import import_rom
from romarr.platforms import GB, resolve
from romarr.selection import Release, score


def test_a_playstation_4_pkg_is_imported_into_the_ps4_library(tmp_path):
    platform = resolve("PlayStation 4")
    assert platform is not None, "PlayStation 4 is not a supported platform"

    download = tmp_path / "download"
    download.mkdir()
    package = download / "God.of.War.III.Remastered.PS4-CUSA01623.pkg"
    package.write_bytes(b"PS4 package")

    result = import_rom(download, platform, tmp_path / "library")[0]

    assert result.ok
    assert result.destination == tmp_path / "library" / "ps4" / package.name
    assert result.destination.read_bytes() == b"PS4 package"


def test_a_playstation_4_iso_is_imported_into_the_ps4_library(tmp_path):
    platform = resolve("PS4")
    download = tmp_path / "God.of.War"
    download.mkdir()
    image = download / "God.of.War.iso"
    image.write_bytes(b"PS4 disc")

    result = import_rom(download, platform, tmp_path / "library")[0]

    assert result.ok
    assert result.destination == tmp_path / "library" / "ps4" / image.name


def test_a_full_size_playstation_4_package_is_not_rejected_as_too_large():
    release = Release(
        title="God of War III Remastered PlayStation 4",
        size=40 * GB,
        seeders=1,
        categories=(1180,),
        download_url="magnet:?xt=urn:btih:" + "A" * 40,
        protocol="torrent",
        indexer="BlueRoms",
    )

    assert score(release, "God of War III Remastered", resolve("PS4")) > 0
