from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPENDIX = PROJECT_ROOT / "docs" / "appendix_asymptotic_theory_20260819.md"


def test_appendix_has_no_embedded_control_characters():
    data = APPENDIX.read_bytes()
    forbidden = {byte for byte in data if byte < 32 and byte not in {9, 10}}
    assert forbidden == set()


def test_primary_rho_theorem_uses_fourth_moments():
    text = APPENDIX.read_text()
    assert "**A5-\\(\\rho\\) (moments for \\(\\rho_P\\)).**" in text
    assert "a^{4+\\eta}+b^{4+\\eta}+(ab)^{2+\\eta}" in text
    assert "Corollary A.2 (moment relaxation at the profile weak null)" in text
    assert "\\frac{\\partial\\rho_P}{\\partial q_a}" in text


def test_equicontinuity_and_plugin_l2_gaps_are_explicitly_resolved():
    text = APPENDIX.read_text()
    assert "Lemma A.3 (random-nuisance empirical-process remainder)" in text
    assert "Lemma A.4 (function-norm consistency)" in text
    assert "Lemma A.5 (in-sample empirical second moment)" in text
    assert "(P_n-P)(\\widehat{IF}^{\\,2}-IF^2)" in text
    assert "\\operatorname{sign}(x-T_X)|y-T_Y|" in text
    assert "u1(|u|<c)" in text


def test_weak_null_permutation_is_not_overclaimed():
    text = APPENDIX.read_text()
    assert "This appendix does not claim that" in text
    assert "combinatorial triangular-array CLT" in text
