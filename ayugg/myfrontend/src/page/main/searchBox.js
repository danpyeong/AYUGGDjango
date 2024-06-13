import { useNavigate } from 'react-router';
import { BodySearchBox, SearchBox, Box, Select, Input, Button, Img } from './mainStyle/searchBoxStyle';
import { useState } from "react";


function Search() {
    let navigate = useNavigate();
    const [inputText, setInputText] = useState('');

    const searchButtonClick = () => {
        const [gameName, tagLine] = inputText.split('#');
        if (gameName && tagLine) {
            navigate(`/search/${gameName}/${tagLine}`);
        } else {
            alert('정확히 입력해주세요!!');
        }
    };

    const activeEnter = (e) => {
        if (e.key === "Enter") {
            searchButtonClick();
        }
    }

    return (
        <BodySearchBox>
            <SearchBox>
                <Box>
                    <Select>
                        <option value="KR">KR</option>
                        <option value="NA">NA</option>
                    </Select>
                    <Input value={inputText} onChange={(e) => { setInputText(e.target.value); }} onKeyDown={activeEnter} />
                    <Button onClick={searchButtonClick} >
                        <Img src={`${process.env.PUBLIC_URL}` + 'assets/images/search-icon/search-icon-24.svg'} />
                    </Button>
                </Box>
            </SearchBox>
        </BodySearchBox>
    );
}

export default Search;