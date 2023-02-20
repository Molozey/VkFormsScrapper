import React from "react";
import DynamicUser from "./DynamicUser";

interface ShowProps {
    number_of_users: number;
}

class ComplexUsers extends React.Component<ShowProps> {
    arr_names: number[]

    constructor(props: ShowProps) {
        super(props);
        this.state = {
            numberOfUser: props.number_of_users
        }

        this.arr_names = new Array(props.number_of_users)
        for(let i = 0; i<this.arr_names.length;i++) {
            this.arr_names[i] = i+1
        }
    }

    render() {
        return (
            <div>
                <h1>Users Cards</h1>
                {this.arr_names.map((content, index) =>
                    <DynamicUser user_id={content} key={index}></DynamicUser>)}
                {/*<DynamicUser user_id={this.arr_names[0]}></DynamicUser>*/}
            </div>
        )
    }
}
export default ComplexUsers