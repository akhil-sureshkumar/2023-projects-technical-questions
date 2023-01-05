import { SetStateAction, Dispatch, FormEvent } from "react";
import Table, { TableContents } from "../Table/Table";

interface AlertModalProps {
    useContents: Dispatch<SetStateAction<TableContents>>,
    contents: TableContents
}

export default function AlertModal({ useContents, contents }: AlertModalProps) {
    function onSubmitEvent(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        // hint: the alert given is at (e.target as any).elements[0].value - ignore typescript being annoying
        var newRows = contents.rowContents
        newRows.push({
            alert: (e.target as any).elements[0].value,
            status: '',
            updates: []
        })
        useContents({
            columnTitles: ['Alert', 'Status', 'Updates'],
            rowContents: newRows
        })

    }

    return (
        <form data-testid='form' onSubmit={onSubmitEvent}>
            <label> Add new alert: </label>
            <input type='text' id='alert' name='alert' />
            <button type='submit'> Add </button>
        </form>
    )
}
