import { ContainerDiv, TierImg, NicknameDiv, TierTextDiv, WinRateGraphDiv, LossRateGraphDiv, WLRDiv} from './multiStyle/resultBoxStyle';
import AddMatchBox from './addMatchBox';
import { tierImgMapping } from '../search/dataHandling/imgMapping';

// input: nickname 1개 output: 결과창 1개
// 한사람의 multisearch의 결괄 나타낸다 
function AddBox(props) {
  return (
    <ContainerDiv>
      <TierImg tier={props.data[0].tier} src={`${process.env.PUBLIC_URL}` + tierImgMapping.get(props.data[0].tier)} />
      <NicknameDiv>{props.data[0].gameName}</NicknameDiv>
      <TierTextDiv>{props.data[0].tier} {props.data[0].rank}</TierTextDiv>
      <WLRDiv>
        <WinRateGraphDiv>{props.data[0].wins}
          <div />
          {props.data[0].tier === 'NONE'
          ? <LossRateGraphDiv data={58}>{props.data[0].losses}</LossRateGraphDiv>
          : <LossRateGraphDiv data={(props.data[0].losses / (props.data[0].losses + props.data[0].wins) * 130 - 7)}>{props.data[0].losses}</LossRateGraphDiv>
          }
        </WinRateGraphDiv>
        {props.data[0].tier === 'NONE'
        ? <div>NONE</div>
        : <div> {Math.round(props.data[0].wins / (props.data[0].losses + props.data[0].wins) * 100)}%</div>}
      </WLRDiv>
      <AddMatchBox value={props.data} />
    </ContainerDiv>
  );
}

export default AddBox;