import pandas as pd
import os
import json


def csv_maker():
    info_sheet = pd.DataFrame(
        columns=['index', 'title', 'filename', 'article_tag', 'article_notag', 'queries', 'summary', 'keywords']
    )

    with open("data/augmented/final.json") as file:
        augmented = json.load(file)

    with open("data/summary/summary_m.json") as file:
        summary = json.load(file)
    # "기타지원_01.html": {
    #     "filename": "기타지원_01.html",
    #     "title": "사회서비스원 긴급돌봄 사업",
    #     "index": 0,
    #     "summary": "요약:\n사회서비스원 긴급돌봄 사업은 코로나19로 인한 돌봄의 필요성과 부재를 해소하기 위해 실시되는 프로그램입니다. 이 프로그램은 확진으로 가정 내 돌봐줄 사람이 부재한 경우, 코로나19로 인한 다른 돌봄서비스가 중단된 경우, 사회복지시설 내 돌봄 인력 공백이 생긴 경우 등에 긴급한 돌봄을 제공합니다.\n\n키워드:\n1. 사회서비스원 #사회복지 #긴급돌봄 #코로나19 #아동돌봄\n2. 대상 구분 #돌봄지원대상 #돌봄이 필요한 층 #긴급한 돌봄\n3. 코로나19 긴급돌봄 #가족돌봄 #보호자 부재 #화이자 백신 접종\n4. 긴급돌봄지원단 #종사자 #인력공백 #보건복지부\n5. 의료기관 #생활치료센터 #입소기간 #자가격리\n6. 갑작스러운 질병 #재가돌봄 #이동지원 #돌봄서비스\n7. 장애등급 #장기요양등급 #돌봄제도권 서비스 #대기\n8. 위기상황 #일시적 돌봄 #가족의무자 부재 #서비스 선정\n9. 시도지사 #시군구청장 #코로나19 확산 #추경 지원\n10. 사회복지센터 #업무 수행 #대책 마련 #지역사회"
    #   },

    for i, doc_dir in enumerate(sorted(os.listdir('data/notags'))):
        tag_dir = os.path.join('data/articles', doc_dir)
        notag_dir = os.path.join('data/notags', doc_dir)
        questions = augmented[doc_dir]['questions']
        info_sheet.loc[i] = [
            i,
            summary[doc_dir]['title'],
            doc_dir,
            tag_dir,
            notag_dir,
            questions,
            summary[doc_dir]['summary_processed'],
            summary[doc_dir]['keywords']
        ]

    info_sheet.to_csv('server/model/info_sheet.csv', index=False)


if __name__ == '__main__':
    csv_maker()
