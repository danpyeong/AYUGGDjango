import { MatchButtons, MatchButton, MoreMatchButton } from "../searchStyle/bottomBoxStyle.js";
import { useState } from "react";
import StatisticBox from "./statisticBox.js";
import { useParams } from 'react-router-dom';
import MatchesBox from "./matchesBox.js";
import { BlankDiv } from "../searchStyle/topBoxStyle.js";
import { useDispatch, useSelector } from "react-redux";
import { fetchDataSuccess } from "../../../redux/dataSlice.js";
import GetStatisticData from "../dataHandling/statisticData.js";

function BottomBox() {
  const [selectedButton, setSelectedButton] = useState('whole');
  const [matchList, setMatchList] = useState([0, 1]);
  const { data } = useSelector((state) => state.data);
  const dispatch = useDispatch();
  const { gameName, tagLine } = useParams();
  
  const handleButtonClick = (buttonName) => {
    setSelectedButton(buttonName);
    setMatchList([0, 1]);

    if (buttonName === 'whole') {
      fetch(`http://localhost:8000/search/${gameName}/${tagLine}`)
      .then(response => response.json())
      .then(data => {
        dispatch(fetchDataSuccess(data));
      })
    } else if (buttonName === 'solo') {
      fetch(`http://localhost:8000/search/${gameName}/${tagLine}`)
      .then(response => response.json())
      .then(_data => {
        let newMatches = [];
        let newmatchNum = [];
        for (let i = 0; i < _data[0].matches.length; i++) {
          if(_data[0].matches[i].info.queueId == 420){
            newMatches.push(_data[0].matches[i]);
            newmatchNum.push(_data[0].matchNum[i])
          }
        }
        if(newMatches.length == 0 ){
          alert("매치 데이터가 존재하지 않습니다.");
          return
        } else {
          _data[0].matches = newMatches;
          _data[0].matchNum = newmatchNum;
          dispatch(fetchDataSuccess(_data));
        }
      }).catch(() => {
          alert("매치 데이터가 존재하지 않습니다.");
          return;
        });
    } else if (buttonName === 'team') {
      fetch(`http://localhost:8000/search/${gameName}/${tagLine}`)
      .then(response => response.json())
      .then(_data => {
        let newMatches = [];
        let newmatchNum = [];
        for (let i = 0; i < _data[0].matches.length; i++) {
          if(_data[0].matches[i].info.queueId == 440){
            newMatches.push(_data[0].matches[i]);
            newmatchNum.push(_data[0].matchNum[i])
          }
        }
        if(newMatches.length == 0 ){
          alert("매치 데이터가 존재하지 않습니다.");
          return
        } else {
          _data[0].matches = newMatches;
          _data[0].matchNum = newmatchNum;
          dispatch(fetchDataSuccess(_data));
        }
      }).catch(() => {
          alert("매치 데이터가 존재하지 않습니다.");
          return
        });
    } else if (buttonName === 'normal') {
      fetch(`http://localhost:8000/search/${gameName}/${tagLine}`)
      .then(response => response.json())
      .then(_data => {
        let newMatches = [];
        let newmatchNum = [];
        for (let i = 0; i < _data[0].matches.length; i++) {
          if(_data[0].matches[i].info.queueId == 490){
            newMatches.push(_data[0].matches[i]);
            newmatchNum.push(_data[0].matchNum[i])
          }
        }
        if(newMatches.length == 0 ){
          alert("매치 데이터가 존재하지 않습니다.");
          return
        } else {
          _data[0].matches = newMatches;
          _data[0].matchNum = newmatchNum;
          dispatch(fetchDataSuccess(_data));
        }
      }).catch(() => {
          alert("매치 데이터가 존재하지 않습니다.");
          return
        });
    }
  };

  const handleMoreButtonClick = () => {
    const newList = [...matchList];

    try {
      if(newList.length == data[0].matches.length ){
        alert("더 이상의 매치를 불러올수 없습니다.");
        return;
      } else {
        newList.push(newList.length);
        setMatchList(newList);
      }
    } catch (error) {
      alert("더 이상의 매치를 불러올수 없습니다.");
      return;
    }
  };

  return (
    <div>
      <MatchButtons>
        <MatchButton value={selectedButton} isclick={'whole'} onClick={() => handleButtonClick('whole')} >전체</MatchButton>
        <MatchButton value={selectedButton} isclick={'solo'} onClick={() => handleButtonClick('solo')} >솔로 랭크</MatchButton>
        <MatchButton value={selectedButton} isclick={'team'} onClick={() => handleButtonClick('team')} >자유 랭크</MatchButton>
        <MatchButton value={selectedButton} isclick={'normal'} onClick={() => handleButtonClick('normal')} >일반</MatchButton>
      </MatchButtons>
      <BlankDiv />
      {data && <StatisticBox data={GetStatisticData(data)} />}
      <BlankDiv />
      <BlankDiv />
      {matchList && <MatchesBox list={matchList} />}
      <MoreMatchButton onClick={handleMoreButtonClick}>MORE +</MoreMatchButton>
    </div>
  );
}

export default BottomBox;