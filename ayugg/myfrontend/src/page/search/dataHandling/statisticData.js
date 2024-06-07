export default function GetStatisticData(data) {
  let resData = {};
  resData.first = {};
  resData.first.wins = 0;
  resData.first.losses = 0;
  resData.first.kills = 0;
  resData.first.deaths = 0;
  resData.first.assists = 0;
  resData.first.teamkills = 0;
  resData.second = [];
  resData.secondTotal = {};
  resData.third = [0,0,0,0,0]; //가한 피해량, 받은 피해량, 분당 골드량, 시야점수, 스킬 명중률
  let index = 0;
  let secondList = [];
  resData.totalMatch = 0;
  

  data[0].matches.forEach(element => {

    // console.log(element.info.participants[data[0].matchNum[index]])
    if (element.info.participants[data[0].matchNum[index]].win) {
      resData.first.wins++;
    } else {
      resData.first.losses++;
    }
    resData.first.kills += element.info.participants[data[0].matchNum[index]].kills;
    resData.first.deaths += element.info.participants[data[0].matchNum[index]].deaths;
    resData.first.assists += element.info.participants[data[0].matchNum[index]].assists;

    if (data[0].matchNum[index] < 5) {
      resData.first.teamkills += element.info.teams[0].objectives.champion.kills;
    } else {
      resData.first.teamkills += element.info.teams[1].objectives.champion.kills;
    }

    let secondData = new Object();
    secondData.championName = element.info.participants[data[0].matchNum[index]].championName;
    secondData.kills = element.info.participants[data[0].matchNum[index]].kills;
    secondData.deaths = element.info.participants[data[0].matchNum[index]].deaths;
    secondData.assists = element.info.participants[data[0].matchNum[index]].assists;
    secondData.cs = element.info.participants[data[0].matchNum[index]].totalMinionsKilled + element.info.participants[data[0].matchNum[index]].neutralMinionsKilled;
    if (element.info.participants[data[0].matchNum[index]].win) {
      secondData.win = 1;
    } else {
      secondData.win = 0;
    }
    secondList.push(secondData);
      
    resData.third[0] += element.info.participants[data[0].matchNum[index]].challenges.teamDamagePercentage;
    resData.third[1] += element.info.participants[data[0].matchNum[index]].challenges.damageTakenOnTeamPercentage;
    resData.third[2] += element.info.participants[data[0].matchNum[index]].challenges.goldPerMinute;
    resData.third[3] += element.info.participants[data[0].matchNum[index]].challenges.visionScorePerMinute;
    
    if(element.info.participants[data[0].matchNum[index]].challenges.skillshotsHit + element.info.participants[data[0].matchNum[index]].challenges.skillshotsDodged != 0){
      resData.third[4] += element.info.participants[data[0].matchNum[index]].challenges.skillshotsHit / (element.info.participants[data[0].matchNum[index]].challenges.skillshotsHit + element.info.participants[data[0].matchNum[index]].challenges.skillshotsDodged);
    }


    index++;
  });

  resData.second = FilterList(secondList);
  resData.totalMatch = secondList.length;
  resData.secondTotal = SecondTotal(secondList);


  return resData;
}

function FilterList(list) {
  if (list.length < 2) {
    return list;
  } else {
    const listObjects = new Map();

    list.forEach((li) => {
      if (listObjects.has(li.championName)) {
        const hasObject = listObjects.get(li.championName);
        hasObject.kills += li.kills;
        hasObject.deaths += li.deaths;
        hasObject.assists += li.assists;
        hasObject.cs += li.cs;
        hasObject.win += li.win;
        hasObject.count += 1;
      } else {
        listObjects.set(li.championName, { ...li, count: 1 });
      }
    });
    return Array.from(listObjects.values()).sort((a, b) => b.count - a.count).slice(0,3);
  }
}

function SecondTotal(list) {
  const total = {
    kills: 0,
    deaths: 0,
    assists: 0,
    cs: 0,
    win: 0,
    count: 0,
  };
  list.forEach((li) => {
    total.kills += li.kills;
    total.deaths += li.deaths;
    total.assists += li.assists;
    total.cs += li.cs;
    total.win += li.win;
    total.count += 1;
  });
  return total;
}