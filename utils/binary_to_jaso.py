from utils.binary_jaso_mapping import (CHOSEONG, 
                                DOUBLE,
                                SHORT_WORD,
                                JUNGSEONG,
                                DOUBLE_JUNGSUNG,
                                JONGSEONG,
                                DOUBLE_JONGSUNG,
                                SHORT_DIRECT_MAPPING
                                )
from typing import List

def jaso2char(l: List)->str:
    result = []
    skip_next = False  # 다음 원소를 건너뛸지 여부를 저장하는 플래그
    print(l)
    for m in range(len(l)):
        if skip_next:
            skip_next = False  # 이전에 m+1을 건너뛰기로 했으면 이번 루프는 처리하지 않고 넘김
            continue

        if l[m] in CHOSEONG:
            if m + 1 < len(l) and l[m] == '000001' and l[m+1] in CHOSEONG:
                result.append(DOUBLE[l[m+1]])
                skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
            elif m + 1 < len(l) and l[m+1] in DOUBLE:  # 된소리(초성) 처리
                combined_s = l[m]  
                result.append(DOUBLE[combined_s])  
                skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
                
            elif m + 1 < len(l) and l[m] in SHORT_WORD and (l[m+1] in JONGSEONG or l[m+1] in CHOSEONG):  # 약어 처리
                short_word = l[m]
                result += SHORT_WORD[short_word]
            else:
                result.append(CHOSEONG[l[m]])

        elif l[m] in JUNGSEONG:
            if (0 < m - 1 or m == 0 )and l[m-1] not in CHOSEONG: # 'ㅇ' 이 초성으로 올경우 추가 처리
                result.append('ㅇ')
            
            if m + 1 < len(l) and l[m+1] == '111010':  # 이중 모음 체크
                result.append(DOUBLE_JUNGSUNG[l[m]])
                skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
            else:
                result.append(JUNGSEONG[l[m]])

        elif l[m] in JONGSEONG:
            if m + 1 < len(l) and l[m+1] in JONGSEONG:
                combined_e = l[m] + l[m+1]
                if combined_e in DOUBLE_JONGSUNG:
                    result.append(DOUBLE_JONGSUNG[combined_e])
                    skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
                else:
                    result.append(JONGSEONG[l[m]])
            else:
                result.append(JONGSEONG[l[m]])

        elif l[m] in SHORT_DIRECT_MAPPING:
            result += SHORT_DIRECT_MAPPING[l[m]]
    
    return result