import awkward as ak
import numpy as np


def ep_pair_mass(e, p):
    m2 = (
        (e.rcene + p.rcene) ** 2
        - (e.rcmox + p.rcmox) ** 2
        - (e.rcmoy + p.rcmoy) ** 2
        - (e.rcmoz + p.rcmoz) ** 2
    )
    assert ak.min(m2) > -0.001, f"{ak.min(m2)=}"
    return np.sqrt(np.abs(m2)) * (m2 > 0)


def ep_recoil_mass(e, p):
    m2 = (
        (250 - e.rcene - p.rcene) ** 2
        - (e.rcmox + p.rcmox) ** 2
        - (e.rcmoy + p.rcmoy) ** 2
        - (e.rcmoz + p.rcmoz) ** 2
    )
    # This is actually allowed to be highly negative.
    # assert ak.min(m2) > -0.001, f"{ak.min(m2)=}"
    return np.sqrt(np.abs(m2)) * (m2 > 0)


class HiggsLike:
    def __init__(self, rc):
        self._idxs = ak.argcartesian([rc.rctyp]).slot0
        id_ep = self._idxs[rc.rctyp == 11]
        id_em = self._idxs[rc.rctyp == -11]
        id_pair = ak.cartesian([id_ep, id_em], axis=1)
        has_pair = ak.num(id_pair) > 0

        self.m_pair_all = ep_pair_mass(rc[id_pair.slot0], rc[id_pair.slot1])
        self.m_recoil_all = ep_recoil_mass(rc[id_pair.slot0], rc[id_pair.slot1])

        self.rc = rc
        self.has_pair = has_pair
        self._id_pair = id_pair

    def _get_best_id_from_pair_slot(self, id_slot, pos_best):
        x = id_slot[ak.singletons(pos_best)]  # To match the shape of .slot0
        x = ak.firsts(x)  # Flatten it, for comparison step.
        x = ak.fill_none(x, -1)  # Replace None with a value that never appears.
        return x

    def apply_chi2(self, fct_chi2):
        self.chi2 = fct_chi2(self.m_pair_all, self.m_recoil_all)
        pos_best = ak.argmin(self.chi2, axis=1)
        id0 = self._get_best_id_from_pair_slot(self._id_pair.slot0, pos_best)
        id1 = self._get_best_id_from_pair_slot(self._id_pair.slot1, pos_best)
        self.rc["is_recoil"] = (self._idxs == id0) | (self._idxs == id1)
        n_recoil_unique = np.unique(ak.sum(self.rc["is_recoil"], axis=1))
        assert set(n_recoil_unique).issubset([0, 2]), f"{n_recoil_unique=}"
