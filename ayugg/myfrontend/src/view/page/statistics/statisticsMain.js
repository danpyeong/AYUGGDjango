import { getChampionStat } from "../../../model/api/statistics";
import { useEffect } from "react";
import { useState } from "react";
import Nav from "../../nav";
import { lineButtons, tierButtons } from "./filterData";
import * as styled from "./statisticsStyle";
import ProgressBar1 from "./progressBar";

function StatisticsMain(){
    const [cham, setCham]=useState([]);
    const [line, setLine]=useState('all');
    const [tier, setTier]=useState('plattinum');

    useEffect(()=>{
        getChampionStat(tier,line)
        .then((data)=>{
            setCham(JSON.parse(data));
            console.log(data);
        });
    },[tier, line]);

    function handleLine(e){
        setLine(e.target.value);
    }

    function handleTier(e){
        setTier(e.target.value);
    }

    function get_img(img){
        return 'https://ddragon.leagueoflegends.com/cdn/14.11.1/img/champion/'+ img
    }

    return (
        <div>
            <Nav></Nav>
            <styled.FilTable>
                <styled.Tr>
                    <styled.Filth>티어</styled.Filth>
                    <styled.FilTd>{tier.toUpperCase()}</styled.FilTd>
                    <td>
                        <styled.FilDiv>
                            {tierButtons.map((info, index)=>{
                                return(
                                    <>
                                        <styled.Button1 key={index} value={info.value} onClick={handleTier}>
                                            {info.name}
                                        </styled.Button1>
                                    </>
                                );
                            })}
                        </styled.FilDiv>
                    </td>
                </styled.Tr>
                <styled.Tr>
                    <styled.Filth>포지션</styled.Filth>
                    <styled.FilTd>{line.toUpperCase()}</styled.FilTd>
                    <td>
                        <styled.FilDiv>
                            {lineButtons.map((info, index)=>{
                                return(
                                    <>
                                        <styled.Button1 key={index} value={info.value} onClick={handleLine}>
                                            {info.name}
                                        </styled.Button1>
                                    </>
                                );
                            })}
                        </styled.FilDiv>
                    </td>
                </styled.Tr>
            </styled.FilTable>
            
            <styled.Table>
                <styled.Tr>
                    <styled.Th>순위</styled.Th>
                    <styled.Th>챔피언</styled.Th>
                    <styled.Th>플레이 수</styled.Th>
                    <styled.Th>평점</styled.Th>
                    <styled.Th>승률</styled.Th>
                    <styled.Th>픽률</styled.Th>
                    <styled.Th>밴률</styled.Th>
                    <styled.Th>cs</styled.Th>
                    <styled.Th>골드</styled.Th>
                </styled.Tr>
                {cham.map((raw,index)=>{
                    let info = raw.fields
                    console.log(info)
                    const iwin = info.statics_win.split('%')[0];
                    const ipicks = info.statics_pick.split('%')[0];
                    const ibanned = info.statics_ban.split('%')[0];
                    let play = info.statics_play
                    return(
                        <styled.Tr key={index}>
                            <styled.Td>{info.statics_ranking}</styled.Td>
                            <styled.TdName>
                                <styled.IconImage src={get_img(info.statics_champ_img)}></styled.IconImage>
                                <styled.NameSpan>{info.statics_champ_name}</styled.NameSpan>
                            </styled.TdName>
                            <styled.Td>{play}</styled.Td>
                            <styled.Td>{info.statics_kda}</styled.Td>
                            <styled.Tds>
                                <styled.MainDiv>
                                    <div>
                                        <ProgressBar1 bgcolor="#3490E5" progress={iwin} height={15}/>
                                    </div>
                                    <div>{iwin}</div>
                                </styled.MainDiv>                                
                            </styled.Tds>
                            <styled.Tds>
                                <styled.MainDiv>
                                    <div>
                                        <ProgressBar1 bgcolor="#DBC926" progress={ipicks} height={15} />
                                    </div>
                                    <div>{ipicks}</div>
                                </styled.MainDiv>                                
                            </styled.Tds>
                            <styled.Tds>
                                <styled.MainDiv>
                                    <div>
                                        <ProgressBar1 bgcolor="#E64638" progress={ibanned} height={15}/>
                                    </div>
                                    <div>{ibanned}</div>
                                </styled.MainDiv>                                
                            </styled.Tds>
                            <styled.Td>{info.statics_cs}</styled.Td>
                            <styled.Td>{info.statics_gold}G</styled.Td>
                        </styled.Tr>
                    );
                })}
            </styled.Table>
        </div>
    );
}

export default StatisticsMain;