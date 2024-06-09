import { UserDiv, FirstDiv, PlayerIconImg, NicknameSpan, TagSpan, SecondDiv, TierDiv, NowTierDiv, TierNameDiv, TierImg, TierListUl, NowTierLi, LabelDiv, OptionItemLi, MoreListUl, GraphBox, MoreImg } from "../searchStyle/topBoxStyle";
import { tierImgMapping } from '../dataHandling/imgMapping';
import { useState } from "react";
import LineTierChart from "../charts/lineTier";
import { useSelector } from "react-redux";
import { GetPlayerIconImg } from "../dataHandling/filterData";
import { ChartCrawlingData, FilterCrawlingData } from "../dataHandling/crawkingDataToList";

//버튼전까지의 UI구성
function TopBox() {
  const { data } = useSelector((state) => state.data);
  const [isDropdownVisible, setDropdownVisible] = useState('false');
  const crawlingData = "S2023 S1 Master\nS2022 Challenger\nS2021 Grandmaster\nS2020 Grandmaster\nS9 Challenger\nS8 Challenger\nS7 Master"; // 실시간 크롤링 불가하여 더미데이터로
  const [tierList, setTierList] = useState([]);

  const clickDropdown = () => {
    if (isDropdownVisible === 'true') {
      setDropdownVisible('false');
    } else {
      setDropdownVisible('true');
      setTierList(FilterCrawlingData(crawlingData));
    }
  };

  return (
    <div>
      {data && <UserDiv>
        <FirstDiv>
          <NicknameSpan>{data[0].gameName} </NicknameSpan>
          <TagSpan>#{data[0].tagLine}</TagSpan>
          <PlayerIconImg src={GetPlayerIconImg(data[0].profileIconId)} />
        </FirstDiv>
        {data[0].tier === 'NONE'
          ? <SecondDiv>
            <TierDiv>
              <NowTierDiv>
                <TierImg src={`${process.env.PUBLIC_URL}/` + tierImgMapping.get(data[0].tier)} tier={data[0].tier}/>
                <div>
                  <TierNameDiv>UNRANK</TierNameDiv>
                  <div></div>
                  <div>승률 집계 불가</div>
                </div>
              </NowTierDiv>
              <TierListUl>
                <li>
                  <div>
                    <LabelDiv onClick={clickDropdown}>
                      <b style={{ paddingLeft: '8px' }}>MORE</b>
                      <MoreImg src={`${process.env.PUBLIC_URL}` + '/assets/images/arrow-down-icon-original.svg'} />
                    </LabelDiv>
                    <MoreListUl isvisible={isDropdownVisible}>
                      {tierList.map(element => {
                        return (<OptionItemLi>
                          <b>{element[0]} </b>
                          <span>{element[1]}</span>
                        </OptionItemLi>);
                      })}
                    </MoreListUl>
                  </div>
                </li>
              </TierListUl>
            </TierDiv>
            <GraphBox>
              <LineTierChart data={ChartCrawlingData(FilterCrawlingData(crawlingData))}></LineTierChart>
            </GraphBox>
          </SecondDiv>
          : <SecondDiv>
            <TierDiv>
              <NowTierDiv>
                <TierImg src={`${process.env.PUBLIC_URL}/` + tierImgMapping.get(data[0].tier)} tier={data[0].tier}/>
                <div>
                  <TierNameDiv>{data[0].tier} {data[0].rank}</TierNameDiv>
                  <div>{data[0].leaguePoints}LP</div>
                  <div>승률 {Math.round(data[0].wins / (data[0].wins + data[0].losses) * 100)}% {'('}{data[0].wins}승 {data[0].losses}{'패)'}</div>
                </div>
              </NowTierDiv>
              <TierListUl>
                <NowTierLi>
                  <b>S24  </b>
                  <span>{data[0].tier} {data[0].rank}</span>
                </NowTierLi>
                <li>
                  <div>
                    <LabelDiv onClick={clickDropdown}>
                      <b style={{ paddingLeft: '8px' }}>MORE</b>
                      <MoreImg src={`${process.env.PUBLIC_URL}` + '/assets/images/arrow-down-icon-original.svg'} />
                    </LabelDiv>
                    <MoreListUl isvisible={isDropdownVisible}>
                      {tierList.map(element => {
                        return (<OptionItemLi>
                          <b>{element[0]} </b>
                          <span>{element[1]}</span>
                        </OptionItemLi>);
                      })}
                    </MoreListUl>
                  </div>
                </li>
              </TierListUl>
            </TierDiv>
            <GraphBox>
              <LineTierChart data={ChartCrawlingData(FilterCrawlingData(crawlingData))}></LineTierChart>
            </GraphBox>
          </SecondDiv>}
      </UserDiv>}
    </div>
  );
}

export default TopBox;