from asyncio.log import logger
from checkov.circleci_pipelines.base_circleci_pipelines_check import BaseCircleCIPipelinesCheck
from checkov.common.models.enums import CheckResult
from checkov.yaml_doc.enums import BlockType

class PreventVolatileOrbs(BaseCircleCIPipelinesCheck):
    def __init__(self):
        name = "Ensure unversioned volatile orbs are not used."
        id = "CKV_CIRCLECIPIPELINES_4"
        super().__init__(
            name=name,
            id=id,
            block_type=BlockType.ARRAY,
            supported_entities=["orbs.{orbs: @}"]
        )

    def scan_entity_conf(self, conf):
        badOrbInBlock = False
        for orb in conf:
            if type(conf[orb]) == str:
                #Special __ vars show up in this dict too.
                if "@volatile" in conf[orb]:
                    badOrbInBlock = True
                    # We only get one return per orb: section, regardless of how many orbs, so set a flag and error later.
                    # Potentially more JMEpath reflection-foo can resolve this so we end up with a call to scan_entity_conf per orb.
        
        if badOrbInBlock:
            return CheckResult.FAILED, conf
        else:
            return CheckResult.PASSED, conf

check = PreventVolatileOrbs()
