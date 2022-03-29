# Build MyLCTuple

The initial versions of `lctuple_DST.xml` and `GearOutput.xml` are copies of: https://github.com/iLCSoft/LCTuple/commit/811e6a46cfe87ba5fc2f3877bf576983f686dde4.

## Usage

```bash
if [ ! -f lctuple_DST.xml ]; then wget https://gist.githubusercontent.com/kunathj/d87d6c8b1821cf7d1f80876d6884577c/raw/lctuple_DST.xml; fi
if [ ! -f GearOutput.xml ]; then wget https://gist.githubusercontent.com/kunathj/d87d6c8b1821cf7d1f80876d6884577c/raw/; fi
source /cvmfs/ilc.desy.de/sw/x86_64_gcc82_centos7/v02-02-03/init_ilcsoft.sh
Marlin lctuple_DST.xml --global.LCIOInputFiles=rv02-02.sv02-02.mILD_l5_o1_v02.E250-SetA.I500002.P2f_z_eehiq.eL.pR.n000.d_dstm_15783_0.slcio --global.MaxRecordNumber=100
--MyAIDAProcessor.FileName=P2f_z_eehiq
rm lctuple_DST.xml GearOutput.xml  # Cleanup
```

It is a good idea to start a test run with a small `MaxRecordNumber`.
You might get a warning that the detector model is inconsitent:

```
[ WARNING "Marlin"]  =============================================================
[ WARNING "Marlin"]  ProcessorMgr::processRunHeader : inconsistent detector models :
[ WARNING "Marlin"]  in lcio : ILD_l5_v02 <=> in gear file : ILD_o1_v05
[ WARNING "Marlin"]  =============================================================
```
The required gear file can be download from: https://github.com/iLCSoft/ILDConfig/tree/master/StandardConfig/production/Gear. E.g.:

```
curl https://raw.githubusercontent.com/iLCSoft/ILDConfig/master/StandardConfig/production/Gear/gear_ILD_l5_v02.xml > GearOutput.xml
```
