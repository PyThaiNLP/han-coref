from fastcoref import TrainingArgs, CorefTrainer
import spacy
import spacy_pythainlp.core

nlp = spacy.blank("th")

args = TrainingArgs(
    output_dir='xlm-roberta-base-model',
    overwrite_output_dir=True,
    model_name_or_path='xlm-roberta-base',
    device='cuda',
    epochs=200,
    logging_steps=115,
    eval_steps=115,
    #max_tokens_in_batch=800
)

trainer = CorefTrainer(
    args=args,
    train_file='dataset/train_2152023_newmm.jsonlines',
    dev_file='dataset/val_2152023_newmm.jsonlines',
    nlp=nlp,
    test_file='dataset/test_2152023_newmm.jsonlines'
)

trainer.train()
