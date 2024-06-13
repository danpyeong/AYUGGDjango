import React, { useEffect, useState } from 'react';
import Nav from '../../nav';
import * as styled from './rakingMainstyle';



const StatusTableRowItem = (props) => {
    const { gameName, tagLine, tier, rank, leaguePoints } = props.data;
    console.log(props.data)
  
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

function Status(props){

    return(
        <styled.Container >
            <styled.StatusTable>
                {props.value ==='solo' ? <span>솔로랭크</span> : <span>자유랭크</span>}
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
            </styled.StatusTable>
            
        </styled.Container>
    );
}


function RankingMain(){

  const [solo , setSolo] = useState([]);
  const [flex , setFlex] = useState([]);

  useEffect(()=>{
    fetch(`http://localhost:8000/ranking/SoloRankModel/`)
    .then(response => response.json())
    .then(data => {
      setSolo(data);
    })
    fetch(`http://localhost:8000/ranking/FlexRankModel/`)
    .then(response => response.json())
    .then(data => {
      setFlex(data);
    })
  },[]);

    return(
        <div>
            <Nav></Nav>
            <styled.MainDiv>
                <Status info={solo} value='solo'></Status>
                <Status info={flex} value='flex'></Status>
            </styled.MainDiv>
        </div>
    );
}

export default RankingMain;