import mailbox
import pandas as pd


def getbody(message):
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    if body:
        try:
            return body.decode("utf-8")
        except:
            return body.decode("latin-1").encode("utf-8").decode("utf-8")
    else:
        return ""


def mail_to_excel(path_file : str, output_path : str):
    rows = []
    for message in mailbox.mbox(path_file):
        content = getbody(message)
        data_dic = {
            "emissor":message["From"],
            "destinatário":message["To"],
            "data_envio":message["Date"],
            "assunto":message["Subject"],
            "texto_email":content,
        }
        rows.append(data_dic)
    df = pd.DataFrame(rows)
    df.to_excel(output_path + f"{path_file}.xlsx",  engine='xlsxwriter', index=False)

if __name__ == "__main__":
    mail_to_excel("teste", "")