import React, { useEffect, useState } from 'react';
import Nav from '../../nav';
import * as styled from './rakingMainstyle';



const StatusTableRowItem = (props) => {
  const { gameName, tagLine, tier, rank, leaguePoints } = props.data;

  return (
    <styled.StatusTableDataContainer>
      <styled.StatusTableData>
        <styled.RankStatusTableRow>{props.index + 1}</styled.RankStatusTableRow>
        <styled.NickStatusTableRow>{gameName} #{tagLine}</styled.NickStatusTableRow>
        <styled.StatusTableRow>{tier} {rank}</styled.StatusTableRow>
        <styled.StatusTableRow>{leaguePoints}LP</styled.StatusTableRow>
      </styled.StatusTableData>
    </styled.StatusTableDataContainer>
  );
};

function Status(props) {
  const handleClick = async () => {
    const response = await fetch('http://localhost:8000/ranking/fetch-and-save-rank-data/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    let data = await response.json();
    console.log(data);
    alert(data.message);
    props.refreshData();
    window.location.reload();
  };

  return (
    <styled.Container >
      <styled.StatusTable>
        {props.value === 'solo' ? <span>솔로랭크</span> : <span>자유랭크</span>}
        <styled.StatusTableHeader>
          <styled.RankStatusTableRow>순위</styled.RankStatusTableRow>
          <styled.NickStatusTableRow>닉네임</styled.NickStatusTableRow>
          <styled.StatusTableRow>티어</styled.StatusTableRow>
          <styled.StatusTableRow>리그포인트</styled.StatusTableRow>
        </styled.StatusTableHeader>
        <styled.TableBody>
          {(props.info).map((data, index) => (
            <StatusTableRowItem key={index} data={data} index={index} />
          ))}
        </styled.TableBody>
        <styled.StyleLink to={`/ranking/${props.value}`}>자세히보기</styled.StyleLink>
        {props.value === 'solo' ? <styled.RefreshButton onClick={handleClick}>
            <styled.RefreshButtonImg src={`${process.env.PUBLIC_URL}` + '/assets/images/reset-icon.svg'} />
          </styled.RefreshButton> : <></> }
      </styled.StatusTable>

    </styled.Container>
  );
}


function RankingMain() {

  const [solo, setSolo] = useState([]);
  const [flex, setFlex] = useState([]);

  const fetchData = () => {
    fetch('http://localhost:8000/ranking/SoloRankModel/')
      .then(response => response.json())
      .then(data => {
        setSolo(data);
      });
    fetch('http://localhost:8000/ranking/FlexRankModel/')
      .then(response => response.json())
      .then(data => {
        setFlex(data);
      });
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>
      <Nav></Nav>
      <styled.MainDiv>
        <Status info={solo} value='solo' refreshData={fetchData}></Status>
        <Status info={flex} value='flex'></Status>
      </styled.MainDiv>
    </div>
  );
}

export default RankingMain;