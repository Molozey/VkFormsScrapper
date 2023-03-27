import React from 'react';
import fig1 from '../images/QAFigure1.svg';
import fig2 from '../images/QAFigure2.svg';
import fig3 from '../images/QAFigure3.svg';
import fig4 from '../images/QAFigure4.svg';
import '../styles/CardQA.css' ;

interface CardProps {
    card_id: number;
}

class AnswerContent {
    answer_text: string
    constructor(answer_text: string) {
        this.answer_text = answer_text
    }
}

class BackGroundStyle {
    figNum: any
    styleNum: any

    constructor(figNum: number, styleNum: number) {
        this.figNum = figNum
        this.styleNum = styleNum
    }
}
interface CardContent {
    readonly card_id: number;
    card_question: string;
    card_creation_date: string;
    card_number_of_answers: number;
    card_answers: AnswerContent[]
}

class CardQA extends React.Component<CardProps> {
    backGroundStyle: BackGroundStyle
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

    condStyle(card_id: number) {
        if (card_id % 4 == 1) {
            return ['fig1', fig1]
        } else if (card_id % 4 == 2) {
            return ['fig2', fig2]
        } else if (card_id % 4 == 3) {
            return ['fig3', fig3]
        } else {
            return ['fig4', fig4]
        }
    }

    constructor(cardId: CardProps) {
        super(cardId);
        let style_array = this.condStyle(cardId.card_id)
        this.backGroundStyle = new BackGroundStyle(style_array[1], style_array[0])
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
            <div className='mask'>
                <div className='background'>
                    <p className='question'> {cardContent.card_question} </p>
                        {cardContent.card_answers.map((answer: AnswerContent, index: number) => {
                            return (
                                <p className='answer' key={index}> {answer.answer_text} </p>
                            );
                        })}
                <img src={this.backGroundStyle.figNum} className={this.backGroundStyle.styleNum} alt='Unstyled'/>
                </div>
            </div>
        )

    }
}

export default CardQA;

