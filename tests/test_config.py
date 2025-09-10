from otdf_python.config import KASInfo, TDFConfig, get_kas_address


def test_tdf_config_defaults():
    cfg = TDFConfig()
    assert cfg.autoconfigure is True
    assert cfg.default_segment_size == 2 * 1024 * 1024
    assert cfg.tdf_format.name == "JSONFormat"
    assert cfg.integrity_algorithm.name == "HS256"
    assert cfg.segment_integrity_algorithm.name == "GMAC"
    assert cfg.mime_type == "application/octet-stream"
    assert cfg.kas_info_list == []
    assert cfg.split_plan == []
    assert cfg.render_version_info_in_manifest is True


def test_kas_info_str():
    kas = KASInfo(
        url="https://kas.example.com",
        public_key="pubkey",
        kid="kid1",
        default=True,
        algorithm="alg",
    )
    s = str(kas)
    assert "KASInfo{" in s
    assert "kas.example.com" in s


def test_get_kas_address():
    assert get_kas_address("kas.example.com") == "https://kas.example.com:443"
    assert (
        get_kas_address("https://kas.example.com:8443")
        == "https://kas.example.com:8443"
    )
