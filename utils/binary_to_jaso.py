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

def jaso2char(l: List) -> str:
    result = []
    skip_next = False  # 다음 원소를 건너뛸지 여부를 저장하는 플래그
    print(l)
    for m in range(len(l)):
        if skip_next: # skip_next True 이면 이번 루프는 처리하지 않고 넘김
            skip_next = False  
            continue

        try:
            if l[m] in CHOSEONG: # <============ 현재 들어온 자소가 초성(자음자)일 경우 ===============>
                if m + 1 < len(l) and l[m] == '000001' and l[m+1] in CHOSEONG: # 만약 초성 'ㅅ'이 오게되면, 'ㅅ' 바로 다음으로 오는 자소가 초성인지 검사 - 한글점자규정해설서 3항 
                    result.append(DOUBLE[l[m+1]])
                    skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정

                elif m + 1 < len(l) and l[m+1] in DOUBLE:  # 된소리(초성) 처리, 초성글자 뒤에 초성이 오게 되면, 해당 자소와 다음 자소를 검사하고 해싱되는 키 검색 - 한글 점자 규정 해설서 5항 된소리 처리
                    combined_s = l[m]  
                    result.append(DOUBLE[combined_s])  # 키에 해당하는 값으로 변경.
                    skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
                    
                elif m + 1 < len(l) and l[m] in SHORT_WORD and (l[m+1] in JONGSEONG or l[m+1] in CHOSEONG):  # 약어 처리(해당 초성이 약어에 해당되고, 뒤에 종성이나 초성이 올 경우 -> 중성 자소 생략을 의미함.) 한글점자규정해설서 제2장 6절, 12항 - 
                    short_word = l[m]
                    result += SHORT_WORD[short_word] # 약어 키에 해당하는 값으로 해싱후 추가
                else:
                    result.append(CHOSEONG[l[m]]) # 위의 조건식을 모두 통과할 경우 단순 초성으로 처리.

            elif l[m] in JUNGSEONG:# <============ 현재 들어온 자소가 중성(모음자)일 경우 ===============>
                if (0 < m - 1 or m == 0 ) and l[m-1] not in CHOSEONG: # 'ㅇ' 이 단어의 가장 첫 초성으로 올경우, 중성이 어두에 올 경우
                    result.append('ㅇ') # 'ㅇ'을 중성 앞에 추가한다. 
                
                if m + 1 < len(l) and l[m+1] == '111010':  # 이중 모음 체크, 한글 점자규정 1장 3절 7항
                    result.append(DOUBLE_JUNGSUNG[l[m]])
                    skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
                else:
                    result.append(JUNGSEONG[l[m]]) # 이전 조건들에 해당되지 않으면 일반 중성(모음자)로 처리

            elif l[m] in JONGSEONG:# <============ 현재 들어온 자소가 종성(받침자)일 경우 ===============>
                if m + 1 < len(l) and l[m+1] in JONGSEONG: # 해당 자소가 겹받침이 될 가능성이 있는 경우를 검사 한글 점자규정 (1장 2절 5항)
                    combined_e = l[m] + l[m+1] # 다음 자소까지 고려
                    if combined_e in DOUBLE_JONGSUNG: # 만약 겹받침이 가능한 자소이고, 해당 자소가 겹받침일 경우
                        result.append(DOUBLE_JONGSUNG[combined_e])
                        skip_next = True  # 다음 원소를 건너뛰기 위해 플래그 설정
                    else:
                        result.append(JONGSEONG[l[m]])
                else:
                    result.append(JONGSEONG[l[m]])

            elif l[m] in SHORT_DIRECT_MAPPING: # <============ 현재 들어온 자소가 부가적인 요소를 고려하지 않아도 되는 약어일 경우 ===============>
                result += SHORT_DIRECT_MAPPING[l[m]] # 한글점자규정 2장 6절 12항의 표 2행 이후 처리
        
        except KeyError:
            continue  # KeyError가 발생하면 무시하고 다음 단계로 넘어감
    
    return result