# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9787  GET              /                                                dashboard
 11703  GET              /api/abo/status                                  api_abo_status
 11657  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10575  GET              /api/automation/status                           api_automation_status
 10597  POST             /api/automation/toggle                           api_automation_toggle
 18441  GET              /api/channel/categories                          api_channel_categories
 18447  POST             /api/channel/set                                 api_channel_set
 18294  GET              /api/channels/status                             api_channels_status
 17968  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 17951  GET              /api/clips                                       api_clips
 17997  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17876  GET              /api/debug/threads                               api_debug_threads
 11668  GET              /api/events                                      api_events
 11240  GET              /api/events/stream                               api_events_stream
 11067  GET              /api/health                                      api_health
 17910  POST             /api/highlights/config                           api_highlights_config
  9721  POST             /api/login                                       dashboard_login_submit
 11996  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11155  GET              /api/notify/status                               api_notify_status
 11166  POST             /api/notify/test                                 api_notify_test
 11757  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11734  GET              /api/proxy/trend                                 api_proxy_trend
 18017  GET              /api/tts/<fn>                                    api_tts_file
 18743  GET              /api/upload_window                               api_upload_window
 11357  GET              /archive/<int:eid>/download                      archive_download
 11385  GET              /download/<int:recording_id>                     download
 11314  GET              /health                                          health
 17845  GET              /healthz                                         healthz
  9712  GET              /login                                           dashboard_login_page
  9742  GET              /logout                                          dashboard_logout
  9749  GET              /manifest.webmanifest                            pwa_manifest
 18716  GET              /overlay                                         overlay_page
  9773  GET              /pwa-icon-<variant>.png                          pwa_icon
  9759  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (326)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   284  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   269  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   192  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    70  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    77  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   213  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   240  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   200  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   325  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   315  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   350  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 19736  /ai                     
 20209  /ask                    
 19827  /assign_role            
 19873  /ban                    
 20541  /botstats               
 20465  /clearwarns             
 20505  /clip                   
 20490  /clipoftheweek          
 20332  /clips                  
 19788  /create_category        
 19757  /create_channel         
 19816  /create_group           
 19799  /create_role            
 19773  /create_voice           
 20109  /daily                  
 20239  /event                  
 20282  /events                 
 20378  /follow                 
 20362  /help                   
 19862  /kick                   
 20091  /leaderboard            
 20318  /livenow                
 20348  /post_test              
 20179  /profile                
 19897  /purge                  
 20077  /rank                   
 20305  /recstatus              
 19838  /remove_role            
 19750  /restream_status        
 19849  /set_channel_perms      
 20042  /setup_community        
 20060  /setup_targets          
 20404  /stats                  
 19662  /status                 
 20700  /streaminfo             
 20597  /sys_report             
 20573  /sys_unpause            
 19884  /timeout                
 20476  /topstreamers           
 19692  /track                  
 19676  /tracklist              
 20393  /unfollow               
 19725  /untrack                
 20426  /warn                   
 20450  /warnings               
```

## Discord-Events (4)

```
 21198  on_member_join
 21160  on_message
 20787  on_raw_reaction_add
 21233  on_ready
```

## Top-Level-Symbole in bot.py (468 Funktionen, 2 Klassen)

```
  2485-2486   _abo_key
  2506-2524   _abo_probe_dump
 15006-15013  _ad_allowlist
 16147-16153  _agent_for
 16156-16172  _ai_telemetry
 16661-16679  _alert
 21372-21422  _alert_monitor_loop
 21774-21836  _announce_loop
  3427-3430   _anthropic_key
  3437-3439   _anthropic_model
  9465-9468   _arg_int
  2477-2482   _as_dict
 16814-16836  _audio_tap_cmd
  9633-9644   _auth_cookie
  9600-9629   _auth_guard
  1715-1720   _auto_on
 17707-17725  _auto_restream_loop
 22915-22930  _azrael_broadcast_reply
 22815-22837  _azrael_chat_reply
 22798-22812  _azrael_chat_should_reply
 22843-22845  _azrael_gate_cfg
 16177-16191  _azrael_live_state
 18628-18642  _azrael_overlay_state
 16543-16597  _azrael_proactive_loop
 15995-16051  _azrael_reaction_to_chats
 22848-22855  _azrael_reply_all_chats
 22785-22795  _azrael_self_names
 22883-22912  _azrael_send_to
 16197-16218  _azrael_system
 21506-21509  _backup_active
 21587-21600  _backup_loop
 21311-21320  _brain_growth_loop
  9966-9993   _brain_growth_snapshot
  2413-2433   _brain_hint_delay
  6105-6133   _brain_notify
 11219-11236  _browser_push
  6149-6236   _build_daily_summary
  2916-3096   _build_native_cmd
 13192-13379  _build_restream_cmd
  3140-3173   _build_ytdlp_cmd
  4927-4954   _can_stop_tracking
  1828-1850   _capture_set_cookies
 11811-11814  _cfg_get
 11817-11819  _cfg_set
 18402-18437  _channel_set_all
 12350-12353  _chat_connected
 12356-12372  _chat_disconnected
  8184-8195   _chat_is_forum
 12392-12394  _chat_sanitize
 12335-12347  _chat_stat
 12375-12378  _chat_stats_snapshot
  3710-3722   _check_ai_models_sync
 10248-10291  _classify_pool_anonymity
 10294-10311  _classify_pool_anonymity_bg
   822-844    _claude_chat_sync_metered
  9494-9501   _client_ip
 21868-21895  _clip_prune
 21898-21908  _clip_recfile_for
 22449-22455  _clip_should_velocity
 21949-22031  _clip_to_discord
  3603-3612   _close_ai_session
 22961-22976  _cohost_broadcast
 22946-22947  _cohost_cfg
 23002-23014  _cohost_fire_highlight
 22950-22958  _cohost_gate
 22979-22999  _cohost_highlight
 22080-22142  _community_events_loop
  9896-9898   _conv_messages
  6508-6551   _cookie_alarm_loop
  1900-1904   _cookie_autorefresh_info
  1805-1809   _cookie_header
  3916-3928   _create_index_safe
 19075-19181  _crowdsec_status
 19021-19072  _crowdsec_via_lapi
 18925-18943  _cscli_bin
 18952-18965  _cscli_path
  6398-6423   _daily_summary_loop
 18983-19000  _darf_journal_lesen
 21346-21369  _db_maintenance_loop
  6367-6395   _db_vacuum_loop
 15029-15053  _detect_foreign_ad
  1450-1461   _diag_path_owner
 16449-16493  _director_finalize
 17260-17267  _director_for
 16398-16446  _director_mark
 22343-22378  _disc_automod_check
 22319-22322  _disc_state_get
 22325-22332  _disc_state_set
 19519-19523  _discord_invite
 22280-22316  _discord_live_thread
 16600-16612  _discord_notify
 19418-19443  _discord_ops_alert
 22178-22276  _discord_post_user
 19579-21308  _discord_run_once
 19458-19516  _discord_start
 21839-21845  _discord_stop
  6426-6503   _disk_alarm_loop
 24391-24440  _disk_autoclean
 24443-24456  _disk_guard_loop
 12785-12787  _drawtext_chain
 11489-11491  _dump_all_threads
 10174-10237  _enrich_proxies_with_geo
  2045-2089   _ensure_cookie_file_netscape
 19526-19576  _ensure_discord_invite
 22045-22077  _ensure_error_channel
  8243-8246   _ensure_notify_topic
 10418-10455  _ensure_proxy_ready
  8197-8224   _ensure_topic
   687-689    _env_int
   692-694    _env_int_range
 22145-22175  _error_channel_loop
 16645-16658  _event_webhook
 12165-12178  _evolution_loop
  5547-5581   _extract_file_payload
  2161-2163   _extract_urls_from_streamurl_node
 18968-18975  _f2b_sudo_hint
  4427-4437   _fehler_text
 10075-10093  _fetch_proxy_list
 17094-17122  _fetch_tiktok_room_id
   755-758    _ff_cmd
 12951-12956  _find_chromium
  3133-3137   _find_external_recorder
  2166-2168   _find_stream_urls
 11862-11887  _fire_webhooks
  7288-7297   _fork_safe
   855-868    _freeai_chat_sync_metered
 19014-19018  _geo_lookup_ips
  3591-3600   _get_ai_session
  7121-7161   _get_live_info
  2703-2710   _get_resolve_semaphore
  7521-7898   _handle_single_tracking
 24213-24215  _hb
 24218-24235  _hb_while
 12406-12408  _highlight_cfg
 12411-12440  _highlight_observe
 12959-12977  _htmlov_screenshot_cmd
 16838-16848  _httpx_proxy
 11895-11907  _in_quiet_hours
 25282-25313  _install_fast_eventloop
  9360-9414   _install_fast_json
 11494-11510  _install_faulthandler
 17753-17762  _intel_ensure_schema
 17800-17835  _intel_index_loop
 17774-17784  _intel_index_one
 17765-17771  _intel_semantic
  4916-4925   _is_authorized
  7422-7428   _is_dead
  2151-2153   _is_hevc
 19003-19005  _is_private_ip
  1614-1621   _is_process_running
  6135-6146   _is_quiet_hours
  1251-1260   _is_upload_window
  9449-9462   _json_error_handler
  6361-6362   _kick_broadcaster_id
  6273-6315   _kick_follower_count
  6257-6260   _kick_slug
 11008-11039  _kick_user_token
  3965-3968   _kind_from_filename
 11924-11929  _latest_popularity
 17475-17508  _live_react_loop
 17271-17464  _live_react_worker
 16054-16065  _live_transcript_push
 17466-17473  _live_users
 16496-16540  _living_title_loop
 21512-21584  _local_backup_scan
  9431-9445   _log_5xx
 13387-13399  _looks_like_codec_err
 13382-13384  _looks_like_source_expired
  7338-7368   _loop_fehler
 11514-11523  _loop_heartbeat
 24183-24210  _loop_lag_monitor
 11526-11594  _loop_watchdog_thread
 15934-15948  _loyalty_add
 15925-15931  _loyalty_get
 15951-15959  _loyalty_top
 12037-12039  _manual_donations_total
  4634-4653   _manual_status
  7430-7431   _mark_dead
 10694-10710  _marketing_loop
 22862-22880  _maybe_handle_command
 24542-24566  _maybe_hype_clip
  3883-3906   _migrate_columns
 23141-23152  _mod_is_exempt
 23155-23160  _mod_warn_first
 23163-23166  _mod_warn_text
 12205-12213  _modlog
   998-1000   _multistream_targets
  7300-7301   _nc_create_subprocess_exec
  7304-7305   _nc_create_subprocess_shell
 10945-10962  _news_loop
 12232-12234  _normalize_ingest
  2344-2361   _note_check_duration
  8237-8240   _notify_topic_name
 16080-16088  _oracle_memories
 16353-16387  _oracle_memorize
 16091-16104  _oracle_persona
 16073-16077  _oracle_recent_text
 12566-12574  _ov_atomic_write
 12554-12560  _ov_bar
 14932-14944  _ov_clip_text
 12563-12564  _ov_oneline
 18680-18709  _overlay_push
 12905-12948  _overlay_render_size
 12298-12302  _overlay_session_reset
 18644-18647  _overlay_src_ok
 15016-15026  _own_invites
 12900-12902  _parse_size
 19189-19269  _parse_ssh_attacks
  6723-6756   _pause_resume_cmd
  1854-1898   _persist_refreshed_cookies
  1759-1791   _pick_checked_pull_proxy
  9530-9543   _pin_auth_value
  9589-9590   _pin_clear_fail
  9569-9572   _pin_locked
  9575-9586   _pin_note_fail
  9546-9566   _pin_ok
 18538-18563  _piper_pick_model
 18575-18622  _piper_say
 11824-11859  _post_json_threaded
 12879-12897  _probe_video_size
  1642-1659   _proc_is_recorder
 10387-10415  _proxy_pool_refresh_loop
  1725-1756   _proxy_report_recording
 11479-11481  _prune_stall_dumps
 10764-10885  _public_stats
 16616-16642  _push_notify
  9691-9693   _pwa_dir
 10144-10159  _quick_validate_proxy
 11890-11892  _quiet_hours_config
  9656-9689   _rate_guard
 15899-15905  _react_warn
  7208-7247   _reap_proc
  2384-2406   _record_check_outcome
   750-752    _redact_stream_urls
 10314-10384  _refresh_proxy_pool
  2177-2267   _resolve_via_html
  2526-2680   _resolve_via_webcast_api_v2
  2743-2805   _resolve_via_ytdlp
 22489-22618  _resolve_youtube_ingest
 12281-12292  _restream_active_sources
 17125-17224  _restream_chat_guardian
 12443-12515  _restream_chat_push
 12540-12549  _restream_chat_push_async
 12980-13067  _restream_html_overlay_start
 13070-13083  _restream_html_overlay_stop
 12243-12266  _restream_overlay_files
 17512-17544  _restream_platform_state
 17669-17704  _restream_resume_after_restart
 13131-13189  _restream_tts_enqueue_wav
 12841-12873  _restream_tts_feeder
 12838-12839  _restream_tts_fifo_path
 13086-13113  _restream_tts_start
 13115-13129  _restream_tts_stop
 17550-17666  _restream_verify_loop
 21477-21489  _retention_loop
 21471-21474  _retention_scan
  2488-2490   _room_is_abo
  5585-5702   _run_ai_call
 11617-11630  _run_async_from_flask
 19008-19011  _run_priv
 25270-25278  _run_selfcheck_and_exit
 21492-21503  _s3_client
  7457-7508   _safe_send
  4560-4576   _sample_net_throughput
  2436-2463   _schedule_next_check
 21425-21468  _scheduler_loop
  3909-3913   _schema_pk
 11634-11639  _scraper_session
 23169-23208  _screen_full
 11083-11120  _sec_headers
  2156-2158   _select_stream_from_data_section
 25083-25267  _selfcheck
  8249-8283   _send_live_notice
  1274-1278   _should_defer_upload
 21911-21946  _shrink_for_discord
  9696-9708   _sicheres_ziel
 21323-21343  _sicherheits_erinnerung_loop
 24463-24480  _sign_health_check
 24483-24502  _sign_health_loop
  7317-7328   _spawn
 25645-25675  _spawn_from_flask
 16850-17091  _start_chat_listener
 11597-11614  _start_loop_watchdog
 10912-10940  _stats_loop
 10891-10894  _stats_output_path
 10897-10909  _stats_write
  7977-7993   _storage_cleanup_loop
 24522-24529  _story_for
  3195-3201   _stream_url_expiry
  3210-3216   _stream_url_is_fresh
  3203-3208   _stream_url_ttl
 14979-14986  _streamer_persona_get
 12790-12794  _studio_chain
 21609-21731  _system_backup
 21740-21770  _system_backup_loop
 10096-10135  _test_proxy
 10642-10658  _testpush_resolve_live
  7433-7454   _tg_sprache_setzen
  8156-8166   _tg_topics_load_into_mem
  8153-8154   _tg_topics_path
  8168-8175   _tg_topics_save
  9504-9512   _token_ok
  8178-8182   _topic_forget
 11910-11921  _tracking_max_duration
  4173-4187   _tracking_remove_cleanup
  4204-4216   _tracking_resume_cleanup
  1508-1531   _try_attach_file_handler
 18565-18573  _tts_cleanup
 10618-10622  _tunnel_effective
 18061-18114  _twitch_channel_status
 23211-23356  _twitch_chat_loop
 23025-23128  _twitch_eventsub_loop
  1297-1310   _upload_queue_add
  1321-1323   _upload_queue_count
  1280-1289   _upload_queue_load
  1270-1272   _upload_queue_path
  1312-1319   _upload_queue_remove
  1291-1295   _upload_queue_save
  1325-1366   _upload_window_loop
  7181-7188   _uptime_s
 12220-12229  _url_host
   815-819    _usage_record_claude
  7371-7415   _verbindung_verloren
  6318-6349   _viewer_sample_loop
  9593-9596   _wants_html
  7191-7205   _warn_empty_env
 24256-24377  _watchdog_loop
 22764-22772  _wchat_thank_ok
 16684-16714  _whisper_get_model
  7278-7285   _whisper_native_section
 15886-15892  _whisper_pool
 16783-16812  _whisper_segments
 16716-16780  _whisper_transcribe
 12621-12783  _write_restream_overlay
 12583-12618  _write_restream_overlay_async
 23380-23460  _youtube_api_chat_loop
 18117-18220  _youtube_api_status
 18223-18290  _youtube_channel_status
 23463-23624  _youtube_chat_loop
 22624-22637  _youtube_restream_autoconfig
 22640-22664  _youtube_restream_autoconfig_inner
 22731-22759  _youtube_send
 18358-18399  _youtube_set_channel
 22667-22701  _yt_access_token
 22704-22719  _yt_live_chat_id
 22727-22728  _yt_sendrate_cfg
 23359-23374  _yt_timeout
  2727-2728   _ytdlp_detect_available
  2730-2741   _ytdlp_note_result
 11484-11486  _zombie_child_count
  7057-7081   about
  4084-4088   add_ai_log_entry
  4001-4004   add_archive_entry
  4598-4600   add_archive_rule
  4375-4409   add_recording
  4148-4165   add_tracking
  5705-5738   ai
  3736-3787   ai_chat
  3821-3831   ai_history_append
  3833-3838   ai_history_clear
  3810-3819   ai_history_load
  3795-3808   ai_rate_limit_check
  5767-5775   aireset
 16221-16240  azrael_chat
 23629-23751  brain_cmd
  3219-3403   build_recording_cmd
  4168-4171   bulk_add_trackings
  6554-6613   bulkadd
  7996-8136   check_all_trackings
  4220-4232   claim_live_transition
 15056-15818  class KickModerator
 13402-14819  class RestreamManager
 10501-10543  classify_proxy_anonymity
  5813-6011   cleanup
  4852-4858   cleanup_old_recordings
  4366-4373   clear_recording
 22381-22446  clip_moment
  4550-4553   compute_storage_forecast
  6676-6720   cookies_cmd
  4139-4145   count_trackings_for_chat
  4071-4082   decide_preferred_recorder
  4011-4014   delete_archive_entry
  4602-4604   delete_archive_rule
  5242-5389   diag
 23863-23924  einnahmen_cmd
  4544-4547   find_recordings_by_fingerprint
  4032-4048   finish_recording_attempt
  4192-4194   get_all_active_trackings
  4099-4101   get_all_checks
  4411-4414   get_all_recordings
  4493-4495   get_all_tags_with_counts
  4521-4524   get_annotations_for_recording
  4006-4009   get_archive_entry
  4514-4517   get_bookmarked_recordings
  1921-2038   get_cookie_health
  4481-4487   get_event_log
  4055-4069   get_last_recording_attempt
  2808-2913   get_live_status
  4791-4794   get_manual_recordings
  4529-4532   get_or_compute_inspect_sync
  4893-4896   get_outcome_breakdown
  4500-4503   get_priority_poll_interval
  4050-4053   get_recent_recording_attempts
  4416-4419   get_recording_by_id
  4507-4510   get_recording_note
  3537-3560   get_redis
  4128-4131   get_stats
  4846-4850   get_storage_stats
  4622-4624   get_tiktok_status_distribution
  4234-4243   get_tracking_state
  4189-4190   get_trackings_for_group
  4807-4810   get_trash_recordings
  8671-9339   handle_recording_finished
  3931-3956   init_db
  4594-4596   list_archive_rules
  5046-5084   live
  7511-7519   live_check_worker
  3615-3649   llm_chat
  3672-3700   llm_chat_sync
  3657-3669   llm_list_models
  4440-4473   log_event
  1576-1609   log_recording_failure
  6870-6919   logs_cmd
 24570-25073  main
  5741-5764   on_ai_media
  6996-7022   on_ai_reply
  7025-7054   on_azrael_mention
  7086-7116   on_callback
 16246-16350  oracle_handle
  6759-6762   pause_tracking
  4906-4911   profile_keyboard
  6821-6867   quota
  7900-7974   reaper_loop
  4618-4620   record_tiktok_status
  5780-5810   recstatus
  3562-3570   redis_get_json
  3573-3579   redis_set_json
 23927-23937  report_cmd
 10546-10548  report_proxy_result
  2270-2297   resolve_tiktok_live_stream
  4802-4805   restore_recording
  6765-6768   resume_tracking
  4607-4612   run_archive_rules
 23940-24163  run_bot
 11399-11451  run_flask
  4582-4585   sample_bandwidth_for_active
  4091-4097   save_tiktok_check
  4358-4364   set_recording_file
  4197-4201   set_tracking_paused
  4797-4800   soft_delete_recording
  8289-8669   split_and_send_video
  4959-5001   start
  4016-4030   start_recording_attempt
  6014-6052   stats
  4772-4789   stop_manual_recording
  6771-6818   stoprec
  6242-6250   summary_cmd
  6922-6993   sysres
  5391-5535   teststream
  5003-5044   tiktok
  6616-6673   topusers
  5121-5178   track
  5086-5118   track_exact
  5192-5240   tracklist
  4656-4770   trigger_manual_recording
  4319-4356   try_acquire_recording_lock
  4813-4815   universal_search
  5180-5190   untrack
 23754-23860  update_cmd
  4539-4542   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             configure, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
