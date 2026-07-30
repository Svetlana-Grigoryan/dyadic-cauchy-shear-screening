# Пошаговая загрузка проекта в GitHub и Zenodo

## 1. Что отправлять в журнал AMC

Загрузите в редакционную систему:

1. `AMC_final_manuscript.pdf` — основной PDF.
2. `AMC_final_manuscript.tex` — исходник LaTeX.
3. `Supplementary_Material_S1.zip` — единый архив вычислительных материалов.
4. `Cover_Letter_AMC.txt` — сопроводительное письмо.
5. `Response_to_Reviewer.pdf` и `Response_to_Reviewer.tex` — только при ревизии или если редакция просит ответ рецензенту.

Не загружайте в журнал папку `.git`, локальное виртуальное окружение `.venv`, временные LaTeX-файлы (`.aux`, `.log`, `.out`) или системные файлы.

## 2. GitHub: рекомендуемая структура

Используйте содержимое папки `GitHub_Repository/` как корень репозитория. Рекомендуемое имя:

`dyadic-cauchy-shear-screening`

### Через веб-интерфейс GitHub

1. Создайте новый публичный репозиторий без автоматического README, лицензии и `.gitignore`.
2. Нажмите **Add file -> Upload files**.
3. Перетащите всё содержимое `GitHub_Repository/`, а не саму внешнюю папку.
4. Commit message: `Initial reproducibility release for AMC manuscript`.
5. После загрузки проверьте, что на верхнем уровне видны `README.md`, `CITATION.cff`, `.zenodo.json`, `LICENSE`, `src/`, `results/` и `manuscript/`.

### Через командную строку

```bash
cd GitHub_Repository
git init
git add .
git commit -m "Initial reproducibility release for AMC manuscript"
git branch -M main
git remote add origin https://github.com/USERNAME/dyadic-cauchy-shear-screening.git
git push -u origin main
```

После этого создайте релиз GitHub:

1. **Releases -> Draft a new release**.
2. Tag: `v1.0.0`.
3. Title: `v1.0.0 - AMC reproducibility release`.
4. Вставьте текст из `RELEASE_NOTES.md`.
5. Опубликуйте релиз.

## 3. Zenodo через интеграцию GitHub

1. Войдите в Zenodo.
2. В профиле откройте раздел GitHub и подключите аккаунт.
3. Нажмите `Sync now` и включите репозиторий `dyadic-cauchy-shear-screening`.
4. Создайте GitHub release `v1.0.0`. Zenodo автоматически архивирует релиз и создаст запись с DOI.
5. Проверьте импортированные метаданные из `.zenodo.json` и `CITATION.cff`.
6. После публикации Zenodo скопируйте DOI и добавьте его:
   - в `README.md`;
   - в `CITATION.cff`;
   - в раздел Data and code availability рукописи, только если журнал разрешает обновление до принятия;
   - в следующий GitHub release `v1.0.1` или в новую версию Zenodo.

## 4. Zenodo вручную

Если интеграция GitHub не используется:

1. Создайте новый Zenodo upload типа **Software**.
2. Загрузите `Zenodo_Deposit/AMC_Reproducibility_Release_v1.0.0.zip`.
3. Скопируйте поля из `Zenodo_Deposit/ZENODO_METADATA.md`.
4. При необходимости заранее нажмите **Reserve DOI**, вставьте зарезервированный DOI в README/CITATION, пересоберите ZIP и только затем публикуйте запись.
5. Лицензия кода: MIT. Текст рукописи и документация: CC BY 4.0, если это не противоречит издательскому соглашению.

## 5. Проверка перед публикацией

В чистой папке распакуйте релиз и выполните:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python verify_full_certificate.py
python verify_family.py
python verify_aes_serialization.py
python activity_milp_forward_logged.py
python activity_milp_independent.py
python verify_activity_witness.py
python verify_release.py
```

Проверьте, что:

- family scan содержит 252 строки;
- AES использует row-major input/output;
- AES order равен 8;
- fixed-space dimensions равны 16, 32, 64, 128;
- оба MILP дают 25/25 и gap 0;
- witness weight равен 25;
- `verify_release.py` завершает работу строкой `release_integrity OK`;
- `sha256sum -c SHA256SUMS` не выдаёт ошибок.

## 6. Версионирование

- `v1.0.0`: версия, соответствующая отправленной статье.
- `v1.0.1`: только технические исправления без изменения результатов.
- `v1.1.0`: новые вычисления или расширенные сертификаты.
- `v2.0.0`: изменение математической модели или основных утверждений.

Не заменяйте файлы уже опубликованного Zenodo record. Для изменений создавайте новую версию, чтобы прежний DOI оставался воспроизводимым.
