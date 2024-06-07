import * as styled from "../searchStyle/matchesBoxStyle";
import * as fd from "../dataHandling/filterData";
import { useSelector } from "react-redux";
import { useEffect, useState } from "react";
import DetailMatchBox from "./detailMatchBox";
import { useNavigate } from "react-router";

function MatchesBox(props) {
  return (
    <div>
      {props.list.map((num) => {
        return <MatchBox key={num} value={num} />
      })}
    </div>
  );
}
function MatchBox(props) {
  const { data } = useSelector((state) => state.data);
  const matchesIndex = props.value;
  const [spellInfo, setSpellInfo] = useState({});
  const [runeInfo, setRuneInfo] = useState({});
  const [isDropdownVisible, setDropdownVisible] = useState('false');
  let navigate = useNavigate();

  const clickDropdown = () => {
    if (isDropdownVisible === 'true') {
      setDropdownVisible('false');
    } else {
      setDropdownVisible('true');
    }
  };

  useEffect(() => {
    fetch('https://ddragon.leagueoflegends.com/cdn/13.21.1/data/ko_KR/summoner.json')
      .then((response) => response.json())
      .then((data) => {
        setSpellInfo(data.data);
      });
    fetch('https://ddragon.leagueoflegends.com/cdn/13.21.1/data/ko_KR/runesReforged.json')
      .then((response) => response.json())
      .then((data) => {
        setRuneInfo(data);
      });
  }, []);

  const NicknameClick = (_nickname) => {
    if (_nickname === "") {
      alert("SummonerName 의 정보가 없습니다");
    } else {
      navigate('/search', { state: { nickname: _nickname } });
      window.location.reload();
    }
  };

  return (
    <div>
      <div style={{ position: 'relative' }}>
        {data && <styled.MatchDiv time={data[0].matches[matchesIndex].info.gameDuration} win={data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].win}>
          <styled.MatchFirstDiv>
            <styled.Font1Div>{fd.GetQueueType(data[0].matches[matchesIndex].info.queueId)}</styled.Font1Div>
            <styled.Font2Div>{fd.GetMatchDate(data[0].matches[matchesIndex].info.gameStartTimestamp)}</styled.Font2Div>
            <styled.Font2Div>{fd.GetMatchTime(data[0].matches[matchesIndex].info.gameDuration)}</styled.Font2Div>
          </styled.MatchFirstDiv>
          <styled.MatchSecondDiv>
            <styled.ChampImg src={fd.GetChampImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].championName)} />
            <span>
              {spellInfo && <div>
                <styled.Spell1Img src={fd.GetSpellImg(spellInfo, JSON.stringify(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].summoner1Id))} />
                <styled.Spell2Img src={fd.GetSpellImg(spellInfo, JSON.stringify(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].summoner2Id))} />
              </div>}
              {runeInfo && <div>
                <styled.Perk1Img src={fd.GetMainRuneImg(runeInfo, data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].perks.styles[0].style, data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].perks.styles[0].selections[0].perk)} />
                <styled.Perk2Img src={fd.GetSubRuneImg(runeInfo, data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].perks.styles[1].style)} />
              </div>}
            </span>
          </styled.MatchSecondDiv>
          <div>
            <styled.Font1Div>{data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].kills}/{data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].deaths}/{data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].assists}</styled.Font1Div>
            <styled.Font2Div>{data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].deaths === 0
              ? "Perfect"
              : ((data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].kills + data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].assists) / data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].deaths).toFixed(2)}</styled.Font2Div>
          </div>
          <div>
            <styled.KillRateCsDiv>
              <styled.Font2Span1>킬관여 {data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].teamId === 100
                ? Math.floor((data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].kills + data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].assists) / data[0].matches[matchesIndex].info.teams[0].objectives.champion.kills * 100)
                : Math.floor((data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].kills + data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].assists) / data[0].matches[matchesIndex].info.teams[1].objectives.champion.kills * 100)
              }%</styled.Font2Span1>
              <styled.Font2Span2>CS {data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].totalMinionsKilled + data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].neutralMinionsKilled}</styled.Font2Span2>
            </styled.KillRateCsDiv>
            <span>
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item0)} />
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item1)} />
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item2)} />
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item3)} />
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item4)} />
              <styled.ItemImg src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item5)} />
              <styled.Item6Img src={fd.GetItemImg(data[0].matches[matchesIndex].info.participants[data[0].matchNum[matchesIndex]].item6)} />
            </span>
          </div>
          <styled.MatchFifthDiv>
            <styled.PartiListUl>
              {[0, 1, 2, 3, 4].map((num) => {
                return (
                  <li style={{ display: 'flex' }} key={num}>
                    <styled.PartiImg src={fd.GetChampImg(data[0].matches[matchesIndex].info.participants[num].championName)} />
                    <styled.PartiName onClick={() => NicknameClick(data[0].matches[matchesIndex].info.participants[num].summonerName)}>{
                      data[0].matches[matchesIndex].info.participants[num].summonerName === ""
                        ? data[0].matches[matchesIndex].info.participants[num].riotIdGameName
                        : data[0].matches[matchesIndex].info.participants[num].summonerName
                    }</styled.PartiName>
                  </li>
                )
              })}
            </styled.PartiListUl>
            <styled.PartiListUl>
              {[5, 6, 7, 8, 9].map((num) => {
                return (
                  <li style={{ display: 'flex' }} key={num}>
                    <styled.PartiImg src={fd.GetChampImg(data[0].matches[matchesIndex].info.participants[num].championName)} />
                    <styled.PartiName onClick={() => NicknameClick(data[0].matches[matchesIndex].info.participants[num].summonerName)}>{
                      data[0].matches[matchesIndex].info.participants[num].summonerName === ""
                        ? data[0].matches[matchesIndex].info.participants[num].riotIdGameName
                        : data[0].matches[matchesIndex].info.participants[num].summonerName
                    }</styled.PartiName>
                  </li>
                )
              })}
            </styled.PartiListUl>
          </styled.MatchFifthDiv>
          <div />
        </styled.MatchDiv>}
        <styled.OpenDiv onClick={clickDropdown}>
          <styled.OpenImg src={'/assets/images/down-arrow.svg'} />
        </styled.OpenDiv>
      </div>
      <DetailMatchBox isvisible={isDropdownVisible} index={matchesIndex} tierList={data[0].matches[matchesIndex].tierList} />
    </div>
  );
}

export default MatchesBox;