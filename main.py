import firebase_admin
import crawler
from firebase_admin import credentials
from firebase_admin import firestore
import json

## firestore init
cred = credentials.Certificate("./google_service.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

## Lotto document
lotto_ref = db.collection(u'LottoManager').document(u'Lotto')

## 마지막 회차
latest_round = lotto_ref.get().to_dict()['latest_round']

## 당첨 정보 document
winning_ref = lotto_ref.collection(u'WinningInfo')

## crawling
for lotto_round in range(1, int(latest_round) + 1):
    winning_info = crawler.getWinningInfo(lotto_round)
    winning_ref.document(str(lotto_round)).set(winning_info)
    print("completed "+str(lotto_round)+" round")
