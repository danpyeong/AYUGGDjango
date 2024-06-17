export async function postChampion(tier, line){
    const response = await fetch('http://localhost:8100/kim/getdata/po',{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            info: {
                tier: tier,
                line: line,
            }
        }),
    }).catch(error=>console.log('fetch에러사항:',error));
    const data = await response.json();
    return await data;
}

export async function getChampionStat(tier, line) {
    const dataUrl = "http://127.0.0.1:8000/champdata/championAllStatics/";
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
            }
        }),
    }).catch(error=>console.log('fetch에러사항:',error));
    const data = await response.json();
    return await data;
  }