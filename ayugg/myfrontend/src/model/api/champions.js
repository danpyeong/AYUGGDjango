export async function postChampionDetailDataApi(champId){
    const response = await fetch('http://localhost:8100/park/getdata2/po',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Accept': 'application/json'
        },
        body: JSON.stringify({ id : champId }),
    }).catch(error=>console.log('fetch에러사항: ',error));
    const data = await response.json();
    return await data;
}

// Django
export const VersionDataApi = async () => {
  const versionApi = "http://127.0.0.1:8000/champdata/version/";
  
  const response = await fetch(versionApi);
  const resJson = await response.json();
  
  return resJson;
};

export async function RuneApi() {
  const ver = await VersionDataApi();

  const runeUrl = "https://ddragon.leagueoflegends.com/cdn/" + "14.11.1" + "/data/ko_KR/runesReforged.json";
  const response = await fetch(runeUrl);
  const resJson = await response.json();

  return resJson;
}

export async function ChampionDataApi() {
  const dataUrl = "http://127.0.0.1:8000/champdata/champion/";
  try {
    const response = await fetch(dataUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('네트워크 상태가 좋지 않습니다.');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('fetch 동작에 문제 발생 : ', error);
    return null;
  }
}

export async function getChampionBasicDataApi(champId) {
  const response = await fetch('http://127.0.0.1:8000/champdata/championBasic/',{
    method: "POST",
    credentials: 'include',
    headers: {
        "Content-Type": "application/json",
        'Accept': 'application/json'
    },
    body: JSON.stringify({
        info: { id : champId }
    }),
  }).catch(error=>console.log('fetch에러사항: ',error));
  const data = await response.json();
  return await data;
}

export async function getChampionRanking(tier, line, ver) {
  const dataUrl = "http://127.0.0.1:8000/champdata/championStatics/";
  const response = await fetch(dataUrl,{
      method: "POST",
      credentials: 'include',
      headers: {
          "Content-Type": "application/json",
          'Accept': 'application/json'
      },
      body: JSON.stringify({
          info: {
              tier: tier,
              line: line,
              ver: ver,
          }
      }),
  }).catch(error=>console.log('fetch에러사항:',error));
  const data = await response.json();
  return await data;
}

export async function getChampionDetailDataApi(champId){
  const response = await fetch('http://127.0.0.1:8000/champdata/detail/',{
    method: "POST",
    credentials: 'include',
    headers: {
        "Content-Type": "application/json",
        'Accept': 'application/json'
    },
    body: JSON.stringify({
        info: { id : champId }
    }),
  }).catch(error=>console.log('fetch에러사항: ',error));
  const data = await response.json();
  return await data;
}