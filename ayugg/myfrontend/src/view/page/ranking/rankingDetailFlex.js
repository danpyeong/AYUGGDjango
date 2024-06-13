import { useEffect, useState } from "react";
import Nav from "../../nav";
import * as styled from "./rankingstyle";
import ProgressBar from "./progressBar";

function RankingDetailFlex(){
    const [user, setUser]=useState([]);

    useEffect(()=>{
        fetch(`http://localhost:8000/ranking/FlexRankModel/`)
        .then(response => response.json())
        .then(data => {
            setUser(data);
            // console.log(data);
        })
    },[]);


    return (
        <div>
            <Nav></Nav>
            
            <styled.Table>
                <styled.MainTr>
                    <styled.Th>순위</styled.Th>
                    <styled.NameTh>닉네임</styled.NameTh>
                    <styled.Th>티어</styled.Th>
                    <styled.Th>레벨</styled.Th>
                    <styled.Th>리그포인트</styled.Th>
                    <styled.Th>승률</styled.Th>
                    <styled.Th></styled.Th>
                </styled.MainTr>
                {user.map((info,index)=>{
                    return(
                        <styled.MainTr key={index}>
                            <styled.Td>{index+1}</styled.Td>
                            <styled.TdName>
                                <styled.IconImage src={`http://ddragon.leagueoflegends.com/cdn/14.12.1/img/profileicon/${info.profileIconId}.png`}></styled.IconImage>
                                <styled.NameSpan>{info.gameName} #{info.tagLine}</styled.NameSpan>
                            </styled.TdName>
                            <styled.Td>{info.tier}</styled.Td>
                            <styled.Td>{info.summonerLevel}</styled.Td>
                            <styled.Td>{info.leaguePoints} LP</styled.Td>                                                   
                            <styled.TdWins>
                                <ProgressBar progress={Math.ceil((info.wins / (info.wins + info.losses))*100)} win={info.wins} lose={info.losses}/> 
                            </styled.TdWins> 
                            <styled.TdPercent>{Math.ceil((info.wins / (info.wins + info.losses))*100)}%</styled.TdPercent>                           
                            
                        </styled.MainTr>
                    );
                })}
            </styled.Table>
        </div>
    );
}

export default RankingDetailFlex;