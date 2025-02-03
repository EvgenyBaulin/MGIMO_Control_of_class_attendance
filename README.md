### **Гайд для студентов**

---

#### **Регистрация**

1. Перейдите на сайт [mgimo.tarakan-tuc.ru](mgimo.tarakan-tuc.ru) и нажмите **"Регистрация"**.
2. Введите ваш **email**, придумайте имя пользователя и надежный пароль. Если вы знаете название
   вашей группы, выберите её из списка (если группы нет, оставьте поле пустым).
3. Нажмите **"Зарегистрироваться"**.
4. После успешной регистрации войдите в систему, используя указанный email и пароль.

---

#### **Как отмечать посещаемость**

1. **Подойдите к NFC-метке** в аудитории.
2. Включите **NFC** на вашем смартфоне (если не включено).
3. Отсканируйте NFC-метку, прикоснувшись телефоном к ней.
4. Вы автоматически попадёте на страницу с подтверждением.
5. Нажмите кнопку **"Отметить присутствие"**, и система зарегистрирует ваше посещение.

---

#### **Что делать, если произошла ошибка**

1. **Код не найден**:
    - Убедитесь, что лекция действительно идёт сейчас. Если проблема сохраняется, сообщите об этом
      преподавателю.
2. **Посещение уже зарегистрировано**:
    - Не нужно отмечаться повторно. Ваше присутствие уже зафиксировано.
3. **Не удаётся войти в аккаунт**:
    - Убедитесь, что вы ввели правильный email и пароль. Если проблема не решается, используйте
      функцию восстановления пароля.

---

#### **Важные моменты**

- **Опоздания**: Если вы отметились позже, чем через 30 минут от начала лекции, это будет
  зафиксировано как "опоздание".
- **Отсутствие NFC на телефоне**: Сообщите преподавателю, чтобы он мог зафиксировать ваше
  присутствие вручную.
- **Ваши данные**: Вы можете изменить свои настройки (например, пароль) в личном кабинете.

---

### **Гайд для преподавателей**

Добро пожаловать! В этом руководстве вы найдёте пошаговые инструкции для управления группами,
аудиториями, лекциями и просмотра посещаемости студентов.

---

#### **Регистрация**

1. Перейдите на сайт [mgimo.tarakan-tuc.ru](mgimo.tarakan-tuc.ru) и нажмите **"Регистрация"**.
2. Укажите ваш **email**, имя пользователя, надежный пароль и **секретный ключ** (его предоставляет
   администрация).
3. Нажмите **"Зарегистрироваться"**. После успешной регистрации войдите в систему с указанным email
   и паролем.

---

#### **Управление группами**

1. Перейдите в раздел **"Группы"**.
2. Нажмите кнопку **"Создать группу"**, введите её название (например, "Группа 101") и сохраните.
3. Все созданные группы будут отображаться в списке. Студенты смогут выбрать их при регистрации.

---

#### **Управление аудиториями и NFC**

1. Перейдите в раздел **"Аудитории"**.
2. Нажмите **"Создать аудиторию"** и укажите её название (например, "Аудитория 101").
    - Приложение автоматически сгенерирует NFC-код. Его нужно записать на метку в формате `http://mgimo.tarakan-tuc.ru/nfc_attendance.html?code=<NFC_CODE>`

---

#### **Создание лекций**

1. Откройте раздел **"Лекции"**.
2. Нажмите **"Создать лекцию"** и заполните форму:
    - Название лекции (например, "Математика 101").
    - Дата, время начала и окончания.
    - Выберите аудиторию, где будет проходить лекция.
3. Сохраните лекцию, и она появится в списке.

---

#### **Просмотр посещаемости**

1. В разделе **"Отчёты"** выберите нужную лекцию.
2. Отчёт покажет:
    - **Присутствующих вовремя**.
    - **Опоздавших** (отметились позже 30 минут).
    - **Отсутствующих**.
3. Вы можете экспортировать отчёт в CSV или PDF для анализа.

---

#### **Как работает отметка студентов**

- Когда студент сканирует NFC-метку, система проверяет:
    - Существует ли лекция, проходящая в данный момент в указанной аудитории.
    - Если всё совпадает, студент считается "присутствующим".

- Если студент сканирует метку позже 30 минут, он отмечается как "опоздавший".