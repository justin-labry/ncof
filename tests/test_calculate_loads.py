import pytest
import unittest
from unittest.mock import Mock, patch
from typing import Dict, List

# 테스트 대상 함수들 import
from core.nf_load_aggregator import calculate_average_loads, average
from openapi_server.models.nf_load_level_information import NfLoadLevelInformation
from openapi_server.models.nf_status import NfStatus


class TestAggregateFunction(unittest.TestCase):
    """aggregate() 함수에 대한 테스트 클래스"""

    def setUp(self):
        """테스트 전 준비 작업"""
        # 테스트용 NfLoadLevelInformation 객체 생성 헬퍼
        self.create_load_info = self._create_load_info_helper

    def _create_load_info_helper(
        self,
        nf_instance_id: str = "test-instance",
        nf_type: str = "SMF",
        nf_set_id: str = "set-001",
        nf_cpu_usage: int = 0,
        nf_memory_usage: int = 0,
        nf_storage_usage: int = 0,
        nf_load_level_average: int = 0,
        nf_load_levelpeak: int = 0,
        nf_load_avg_in_aoi: int = 0,
    ) -> NfLoadLevelInformation:
        """테스트용 NfLoadLevelInformation 객체 생성"""
        load_info = NfLoadLevelInformation()
        load_info.nf_instance_id = nf_instance_id
        load_info.nf_type = nf_type
        load_info.nf_set_id = nf_set_id
        load_info.nf_status = NfStatus()

        load_info.nf_cpu_usage = nf_cpu_usage
        load_info.nf_memory_usage = nf_memory_usage
        load_info.nf_storage_usage = nf_storage_usage
        load_info.nf_load_level_average = nf_load_level_average
        load_info.nf_load_levelpeak = nf_load_levelpeak
        load_info.nf_load_avg_in_aoi = nf_load_avg_in_aoi
        return load_info

    def test_aggregate_single_instance_complete_data(self):
        """단일 인스턴스, 완전한 데이터에 대한 테스트"""
        # Given: 완전한 데이터를 가진 단일 인스턴스
        load_infos = [
            self.create_load_info(
                nf_cpu_usage=80,
                nf_memory_usage=60,
                nf_storage_usage=40,
                nf_load_level_average=70,
                nf_load_levelpeak=90,
                nf_load_avg_in_aoi=75,
            ),
            self.create_load_info(
                nf_cpu_usage=90,
                nf_memory_usage=70,
                nf_storage_usage=50,
                nf_load_level_average=80,
                nf_load_levelpeak=100,
                nf_load_avg_in_aoi=85,
            ),
            self.create_load_info(
                nf_cpu_usage=70,
                nf_memory_usage=50,
                nf_storage_usage=30,
                nf_load_level_average=60,
                nf_load_levelpeak=80,
                nf_load_avg_in_aoi=65,
            ),
        ]

        input_data = {"instance-001": load_infos}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 결과 검증
        self.assertEqual(len(result), 1)
        aggregated = result[0]

        # 메타데이터 검증
        self.assertEqual(aggregated.nf_instance_id, "instance-001")
        self.assertEqual(aggregated.nf_type, "SMF")
        self.assertEqual(aggregated.nf_set_id, "set-001")
        # self.assertEqual(aggregated.nf_status, "ACTIVE")

        # 집계된 값 검증 (평균값)
        self.assertEqual(aggregated.nf_cpu_usage, 80)  # (80+90+70)/3 = 80
        self.assertEqual(aggregated.nf_memory_usage, 60)  # (60+70+50)/3 = 60
        self.assertEqual(aggregated.nf_storage_usage, 40)  # (40+50+30)/3 = 40
        self.assertEqual(aggregated.nf_load_level_average, 70)  # (70+80+60)/3 = 70
        self.assertEqual(aggregated.nf_load_levelpeak, 90)  # (90+100+80)/3 = 90
        self.assertEqual(aggregated.nf_load_avg_in_aoi, 75)  # (75+85+65)/3 = 75

    def test_aggregate_multiple_instances(self):
        """여러 인스턴스에 대한 테스트"""
        # Given: 두 개의 인스턴스
        input_data = {
            "instance-001": [
                self.create_load_info(
                    nf_instance_id="instance-001", nf_cpu_usage=80, nf_memory_usage=60
                ),
                self.create_load_info(
                    nf_instance_id="instance-001", nf_cpu_usage=90, nf_memory_usage=70
                ),
            ],
            "instance-002": [
                self.create_load_info(
                    nf_instance_id="instance-002",
                    nf_type="UPF",
                    nf_cpu_usage=50,
                    nf_memory_usage=40,
                )
            ],
        }

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 결과 검증
        self.assertEqual(len(result), 2)

        # 인스턴스별로 결과 찾기
        instance_001_result = next(
            r for r in result if r.nf_instance_id == "instance-001"
        )
        instance_002_result = next(
            r for r in result if r.nf_instance_id == "instance-002"
        )

        # instance-001 검증
        self.assertEqual(instance_001_result.nf_cpu_usage, 85)  # (80+90)/2
        self.assertEqual(instance_001_result.nf_memory_usage, 65)  # (60+70)/2
        self.assertEqual(instance_001_result.nf_type, "SMF")

        # instance-002 검증
        # self.assertEqual(instance_002_result.nf_cpu_usage, 50)
        # self.assertEqual(instance_002_result.nf_memory_usage, 40)
        # self.assertEqual(instance_002_result.nf_type, "UPF")

    def _test_aggregate_with_none_values(self):
        """None 값이 포함된 데이터에 대한 테스트"""
        # Given: 일부 필드가 None인 데이터
        load_infos = [
            self.create_load_info(nf_cpu_usage=80, nf_storage_usage=40),  # None 값
            self.create_load_info(
                nf_cpu_usage=90,
                nf_memory_usage=70,  # None 값
            ),
            self.create_load_info(nf_memory_usage=60, nf_storage_usage=50),  # None 값
        ]

        input_data = {"instance-001": load_infos}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: None이 아닌 값들만 평균 계산되는지 검증
        self.assertEqual(len(result), 1)
        aggregated = result[0]

        self.assertEqual(aggregated.nf_cpu_usage, 85)  # (80+90)/2, None 제외
        self.assertEqual(aggregated.nf_memory_usage, 65)  # (70+60)/2, None 제외
        self.assertEqual(aggregated.nf_storage_usage, 45)  # (40+50)/2, None 제외

    def _test_aggregate_with_all_none_values(self):
        """모든 값이 None인 경우 테스트"""
        # Given: 모든 필드가 None인 데이터
        load_infos = [
            self.create_load_info(
                # nf_cpu_usage=None,
                # nf_memory_usage=None,
                # nf_storage_usage=None,
                # nf_load_level_average=None,
                # nf_load_levelpeak=None,
                # nf_load_avg_in_aoi=None,
            )
        ]

        input_data = {"instance-001": load_infos}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 결과가 0으로 설정되는지 검증
        self.assertEqual(len(result), 1)
        aggregated = result[0]

        self.assertEqual(aggregated.nf_cpu_usage, 0)
        self.assertEqual(aggregated.nf_memory_usage, 0)
        self.assertEqual(aggregated.nf_storage_usage, 0)
        self.assertEqual(aggregated.nf_load_level_average, 0)
        self.assertEqual(aggregated.nf_load_levelpeak, 0)
        self.assertEqual(aggregated.nf_load_avg_in_aoi, 0)

    def _test_aggregate_empty_list_per_instance(self):
        """인스턴스별로 빈 리스트가 있는 경우 테스트"""
        # Given: 빈 리스트와 정상 리스트가 혼재
        input_data = {
            "instance-001": [],  # 빈 리스트
            "instance-002": [
                self.create_load_info(nf_instance_id="instance-002", nf_cpu_usage=50)
            ],
        }

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 빈 리스트는 무시되고, 정상 데이터만 처리
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].nf_instance_id, "instance-002")

    def _test_aggregate_empty_input(self):
        """완전히 빈 입력에 대한 테스트"""
        # Given: 빈 딕셔너리
        input_data = {}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 빈 리스트 반환
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def _test_aggregate_rounding_behavior(self):
        """반올림 동작에 대한 테스트"""
        # Given: 평균이 소수점을 가지는 데이터
        load_infos = [
            self.create_load_info(nf_cpu_usage=10),
            self.create_load_info(nf_cpu_usage=20),
            self.create_load_info(nf_cpu_usage=21),  # 평균 17.0
        ]

        input_data = {"instance-001": load_infos}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 소수점 반올림 확인
        self.assertEqual(result[0].nf_cpu_usage, 17)  # 17.0 -> 17

    def _test_aggregate_metadata_consistency(self):
        """메타데이터 일관성 테스트"""
        # Given: 첫 번째 요소의 메타데이터가 사용되는지 확인
        load_infos = [
            self.create_load_info(
                nf_type="SMF", nf_set_id="set-001", nf_status="ACTIVE", nf_cpu_usage=80
            ),
            self.create_load_info(
                nf_type="UPF",  # 다른 값
                nf_set_id="set-002",  # 다른 값
                nf_status="INACTIVE",  # 다른 값
                nf_cpu_usage=90,
            ),
        ]

        input_data = {"instance-001": load_infos}

        # When: aggregate 함수 호출
        result = calculate_average_loads(input_data)

        # Then: 첫 번째 요소의 메타데이터가 사용됨
        aggregated = result[0]
        self.assertEqual(aggregated.nf_type, "SMF")
        self.assertEqual(aggregated.nf_set_id, "set-001")
        self.assertEqual(aggregated.nf_status, "ACTIVE")


class TestAverageFunction(unittest.TestCase):
    """average() 함수에 대한 테스트 클래스"""

    def test_average_normal_case(self):
        """일반적인 경우 테스트"""
        result = average([10, 20, 30])
        self.assertEqual(result, 20.0)

    def test_average_single_value(self):
        """단일 값 테스트"""
        result = average([42])
        self.assertEqual(result, 42.0)

    def test_average_empty_list(self):
        """빈 리스트 테스트"""
        result = average([])
        self.assertEqual(result, 0)

    def test_average_decimal_result(self):
        """소수점 결과 테스트"""
        result = average([10, 20, 21])
        self.assertEqual(result, 17.0)  # 반올림되어 17.00

    def test_average_rounding_precision(self):
        """반올림 정밀도 테스트"""
        result = average([1, 2, 3])
        self.assertEqual(result, 2.0)  # 정확히 2.00

        result = average([1, 2])
        self.assertEqual(result, 1.5)  # 정확히 1.50


if __name__ == "__main__":
    # 개별 테스트 실행 방법
    print("=== aggregate() 함수 테스트 시작 ===")

    # unittest 실행
    unittest.main(verbosity=2)

    # 또는 pytest로 실행하려면:
    # pytest test_aggregate.py -v
