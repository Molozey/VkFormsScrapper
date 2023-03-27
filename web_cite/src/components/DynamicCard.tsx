import React from "react";


interface CardProps {
    card_id: number;

}

class AnswerContent {
    answer_text: string
    constructor(answer_text: string) {
        this.answer_text = answer_text
    }
}

interface CardContent {
    readonly card_id: number;
    card_question: string;
    card_creation_date: string;
    card_number_of_answers: number;
    card_answers: AnswerContent[]


}
class DynamicCard extends React.Component<CardProps>{
    _def_ans: AnswerContent = new AnswerContent('defaultAnswer')
    cardContent: CardContent = {
        card_id: this.props.card_id,
        card_question: "default",
        card_creation_date: "unknown",
        card_number_of_answers: 1,
        card_answers: [this._def_ans]
    }
    public changeState(json: any) : void {
        let _new_ans = json.answers.map((text: string) => {
            return new AnswerContent(text)
        })
        this.setState({
            cardContent: {
                card_id: this.props.card_id,
                card_question: json.form_content,
                card_creation_date: json.form_vk_created_date,
                card_number_of_answers: json.number_of_answers,
                card_answers: _new_ans
            },
            dataIsLoaded: true
        }
        )
    }

    constructor(cardId: CardProps) {
        super(cardId);
        this.state = {
            cardContent: this.cardContent,
            dataIsLoaded: false
        }

        let query: string = `http://127.0.0.1:5000/complex_form?form_id=${this.props.card_id}`
        fetch(query, {
            method: "GET",
            headers: {
                "Access-Control-Allow-Origin": "127.0.0.1:5000"
            }
        })
            .then((res) => res.json())
            .then(async (json) =>
                    this.changeState(json));
        }



    render() {
        // @ts-ignore
        const {cardContent, dataIsLoaded} = this.state;
        if (!dataIsLoaded) return (
            <div>Wait a Little</div>
        )
        return (
            <div className={"cardComplex"}>
                <div>Card ID: {cardContent.card_id}</div>
                <div>Card Title: {cardContent.card_question}</div>
                <div>Card creation date: {cardContent.card_creation_date}</div>
                <div>
                    {cardContent.card_answers.map((answer: AnswerContent, index: number) => {
                        return (
                            <div key={index}>question: {answer.answer_text}</div>
                        );
                    })}
                </div>
            </div>
        )
    }
}
export default DynamicCard