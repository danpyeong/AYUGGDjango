import { MatchDiv, MatchChampImg, KdaDiv, TimeDiv } from './multiStyle/resultBoxStyle';

// input: matchList output: 결과창안의 match 5개
// 1개의 결과창 안의 5개의 match결괄 나타낸다
function AddMatchBox(props) {
  const currentTime = new Date();
  return (
    <div>
      {props.value[0].matches.map((data, index) => (
        <MatchDiv key={index}>
          <MatchChampImg src={(GetChampImg(data.info.participants[index].championName))}/>
          <KdaDiv style={ (data.info.participants[index].win) ? {background: "#D5E3FF", color: "#4171D6"} : {background: "#FFD8D9", color: "#D31A45"}}>
              <div>{data.info.participants[index].kills}/{data.info.participants[index].deaths}/{data.info.participants[index].assists}</div>
          </KdaDiv>
          <TimeDiv>
          {
            Math.floor((currentTime.getTime() - data.info.gameStartTimestamp) / 3600000) < 24
            ? Math.floor((currentTime.getTime() - data.info.gameStartTimestamp) / 3600000) + "시간전"
            : Math.floor((currentTime.getTime() - data.info.gameStartTimestamp) / 3600000 / 24) + "일전"      
          }
          </TimeDiv>
        </MatchDiv>
      ))}
    </div>
  );
}

function GetChampImg(championName) {
  const version = "https://ddragon.leagueoflegends.com/cdn/14.11.1/img/champion/"
  const champUrl = version + championName + ".png";
  return champUrl;
}

export default AddMatchBox;