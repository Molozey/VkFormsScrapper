import React from "react";
import CardQA from "./CardQA";

interface ShowProps {
    number_of_forms: number;
}

class ShowSeveralCards extends React.Component<ShowProps> {
    arr_forms: number[]

    constructor(props: ShowProps) {
        super(props);
        this.state = {
            numberOfUser: props.number_of_forms
        }

        this.arr_forms = new Array(props.number_of_forms)
        for(let i = 0; i<this.arr_forms.length; i++) {
            this.arr_forms[i] = i+1
        }
    }

    render() {
        return (
            <div style={{display: "flex", flexWrap: "wrap", justifyContent: "space-evenly"}}>{
                this.arr_forms.map((content, index) =>
                    <CardQA card_id={content} key={index}/>)
            }</div>
        )
        }
    }
    export default ShowSeveralCards