import firebase_admin
import crawler
import datetime
import utils
from firebase_admin import credentials
from firebase_admin import firestore

# firestore init
cred = credentials.Certificate("./google_service.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Lotto document
lotto_ref = db.collection(u'LottoManager').document(u'Lotto')
# 당첨 정보 document
winning_ref = lotto_ref.collection(u'WinningInfo')
# 마지막 회차
latest_round = lotto_ref.get().to_dict()['latest_round']
# 마지막 업데이트 날짜
update_date = lotto_ref.get().to_dict()['update_date']
# 업데이트 해야 될 횟수
update_count = utils.gab_of_weeks(update_date)
# crawling
if utils.is_saturday() and update_count > 0:
    update_round = int(latest_round)
    for lotto_round in range(int(latest_round) + 1,  int(latest_round) + update_count + 1):
        winning_info = crawler.getWinningInfo(lotto_round)
        winning_ref.document(str(lotto_round)).set(winning_info)
        update_round = lotto_round
        print("completed "+str(lotto_round)+" round")
    lotto_ref.update({
        'latest_round': update_round,
        'update_date': datetime.datetime.now().strftime('%Y-%m-%d')
    })
