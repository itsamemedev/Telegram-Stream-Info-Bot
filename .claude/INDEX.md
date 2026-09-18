# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9517  GET              /                                                dashboard
 11485  GET              /api/abo/status                                  api_abo_status
 11439  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10305  GET              /api/automation/status                           api_automation_status
 10327  POST             /api/automation/toggle                           api_automation_toggle
 18605  GET              /api/channel/categories                          api_channel_categories
 18611  POST             /api/channel/set                                 api_channel_set
 18458  GET              /api/channels/status                             api_channels_status
 18132  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18115  GET              /api/clips                                       api_clips
 18161  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18040  GET              /api/debug/threads                               api_debug_threads
 11450  GET              /api/events                                      api_events
 10964  GET              /api/events/stream                               api_events_stream
 10791  GET              /api/health                                      api_health
 18074  POST             /api/highlights/config                           api_highlights_config
  9451  POST             /api/login                                       dashboard_login_submit
 11775  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 10879  GET              /api/notify/status                               api_notify_status
 10890  POST             /api/notify/test                                 api_notify_test
 11539  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11516  GET              /api/proxy/trend                                 api_proxy_trend
 18181  GET              /api/tts/<fn>                                    api_tts_file
 18956  GET              /api/upload_window                               api_upload_window
 11081  GET              /archive/<int:eid>/download                      archive_download
 11109  GET              /download/<int:recording_id>                     download
 11038  GET              /health                                          health
 17998  GET              /healthz                                         healthz
  9442  GET              /login                                           dashboard_login_page
  9472  GET              /logout                                          dashboard_logout
  9479  GET              /manifest.webmanifest                            pwa_manifest
 18929  GET              /overlay                                         overlay_page
  9503  GET              /pwa-icon-<variant>.png                          pwa_icon
  9489  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (330)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   404  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
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
   381  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   358  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
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
   425  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   329  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   314  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   237  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   193  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   479  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   258  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   285  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   245  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   376  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   396  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   391  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   467  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
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
   410  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
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
   944  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1053  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1081  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1101  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   931  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   993  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   980  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   961  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   329  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   606  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   601  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   649  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   532  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   859  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   623  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   586  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   559  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   833  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   792  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   698  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   631  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   411  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   876  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   499  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   754  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   909  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   894  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   455  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   693  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   679  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   662  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   719  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1244  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1319  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1208  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   812  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   708  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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
   370  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   360  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   395  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   348  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   438  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
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
   371  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
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

## Discord-Slash-Commands in discordbot.py (60)

```
   803  /ai                     
  1207  /ask                    
   904  /assign_role            
   954  /ban                    
  2065  /botstats               
  1466  /clearwarns             
  2029  /clip                   
  2014  /clipoftheweek          
  1333  /clips                  
   859  /create_category        
   830  /create_channel         
   894  /create_group           
   869  /create_role            
   845  /create_voice           
  1090  /daily                  
  1236  /event                  
  1278  /events                 
  1376  /follow                 
  1361  /help                   
   944  /kick                   
  1065  /leaderboard            
  1320  /livenow                
  1348  /post_test              
  1168  /profile                
   976  /purge                  
  1052  /rank                   
  1308  /recstatus              
   914  /remove_role            
   816  /restream_status        
   924  /set_channel_perms      
  1019  /setup_community        
  1036  /setup_targets          
  1408  /stats                  
   733  /status                 
  1537  /streaminfo             
  2117  /sys_aireset            KI-Kontext zurücksetzen (TG: /aireset)
  2119  /sys_bulkadd            Mehrere User tracken (TG: /bulkadd a b c)
  2110  /sys_cleanup            Alte Aufnahmen aufräumen (TG: /cleanup)
  2121  /sys_cookies            Cookie-Status (TG: /cookies)
  2116  /sys_diag               Vollständige Diagnose (TG: /diag)
  2120  /sys_live               Live-Check erzwingen (TG: /live @user)
  2115  /sys_logs               Letzte Fehler-Logs (TG: /logs)
  2107  /sys_pause              Tracking pausieren (TG: /pause @user)
  2111  /sys_quota              Speicher-Quota (TG: /quota)
  1521  /sys_report             
  2112  /sys_res                System-Ressourcen (TG: /sysres)
  2108  /sys_resume             Tracking fortsetzen (TG: /resume @user)
  2109  /sys_stoprec            Aufnahme grazil stoppen (TG: /stoprec @user)
  2114  /sys_summary            Tageszusammenfassung (TG: /summary)
  2118  /sys_teststream         Recorder-Selbsttest (TG: /teststream)
  2113  /sys_topusers           Top-Streamer-Statistik (TG: /topusers)
  1498  /sys_unpause            
   964  /timeout                
  1476  /topstreamers           
   761  /track                  
   746  /tracklist              
  1390  /unfollow               
   793  /untrack                
  1429  /warn                   
  1452  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2274  on_member_join
  2236  on_message
  2143  on_raw_reaction_add
  2309  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (45 Funktionen)

```
  1614-1665   _award_xp
  1834-1863   _clip_week_leader
  1887-1901   _clipoftheweek_loop
  2425-2487   _community_events_loop
  1571-1593   _dc_client
  1596-1605   _dc_offen
  2527-2562   _disc_automod_check
   423-428    _disc_sprache_setzen
  1668-1716   _discord_ai_automod
   556-595    _discord_automod
  1719-1739   _discord_azrael_reply
  1904-2384   _discord_run_once
   258-316    _discord_start
   319-373    _ensure_discord_invite
  2390-2422   _ensure_error_channel
   444-457    _ensure_rank_roles
   692-706    _ensure_team_roles
  2490-2520   _error_channel_loop
   605-609    _guard
   525-553    _handle_voice_ai
   431-441    _is_admin
  1782-1793   _liveboard_loop
   612-630    _on_level_up
   521-522    _par_chat_id
  1866-1884   _post_clip_of_week
  1796-1814   _post_weekly_digest
   460-486    _provision_base_channels
   489-505    _provision_user_channels
  1300-1397   _reg_betrieb
   990-1079   _reg_community_setup
  1082-1157   _reg_daily_profil
  1200-1297   _reg_frage_events
   720-818    _reg_info
   936-987    _reg_moderation
  1160-1197   _reg_profil
   885-933    _reg_rollen
   821-882    _reg_server
  1400-1487   _reg_streamer
  1490-1568   _reg_system
   665-689    _run_tg_handler
   508-518    _tracked_usernames
   163-237    _uebernehmen
  1748-1779   _update_liveboard
  1817-1831   _weekly_digest_loop
   240-243    starte
```

## Top-Level-Symbole in bot.py (499 Funktionen, 2 Klassen)

```
 23244-23266  _abbruch_datenbank_unlesbar
  2576-2577   _abo_key
  2597-2615   _abo_probe_dump
 14953-14960  _ad_allowlist
 15929-15935  _agent_for
 15938-15954  _ai_telemetry
 16449-16467  _alert
 19815-19865  _alert_monitor_loop
 20217-20279  _announce_loop
  3208-3218   _anthropic_key
  3225-3227   _anthropic_model
  9137-9140   _arg_int
  2568-2573   _as_dict
 22994-23003  _async_exc_handler
 16630-16652  _audio_tap_cmd
 17189-17248  _audio_tap_melden
 16666-16690  _audio_tap_sammler
  9305-9374   _auth_cookie
  9272-9301   _auth_guard
  1805-1810   _auto_on
 17860-17878  _auto_restream_loop
 12955-12997  _avatar_frames_laden
 21297-21312  _azrael_broadcast_reply
 21197-21219  _azrael_chat_reply
 21169-21194  _azrael_chat_should_reply
 21225-21227  _azrael_gate_cfg
 15959-15973  _azrael_live_state
 18842-18856  _azrael_overlay_state
 16331-16385  _azrael_proactive_loop
 15777-15833  _azrael_reaction_to_chats
 21230-21237  _azrael_reply_all_chats
 21156-21166  _azrael_self_names
 21265-21294  _azrael_send_to
 12916-12952  _azrael_spricht
 15979-16000  _azrael_system
 19949-19952  _backup_active
 20030-20043  _backup_loop
 23067-23076  _brain_crowdsec_snap
 19736-19745  _brain_growth_loop
  9696-9723   _brain_growth_snapshot
  2510-2530   _brain_hint_delay
 23139-23174  _brain_moderation_snap
  6087-6115   _brain_notify
 23177-23199  _brain_recording_snap
 23079-23136  _brain_restream_health
 23202-23215  _brain_tiktok_status_snap
 10943-10960  _browser_push
  6127-6214   _build_daily_summary
 13276-13280  _build_restream_cmd
  4909-4936   _can_stop_tracking
  1918-1940   _capture_set_cookies
 11593-11596  _cfg_get
 11599-11601  _cfg_set
 18566-18601  _channel_set_all
 12144-12147  _chat_connected
 12150-12166  _chat_disconnected
  8204-8215   _chat_is_forum
 16996-17021  _chat_listener_abbauen
 12186-12188  _chat_sanitize
 12129-12141  _chat_stat
 12169-12172  _chat_stats_snapshot
  3511-3523   _check_ai_models_sync
  9978-10021  _classify_pool_anonymity
 10024-10041  _classify_pool_anonymity_bg
   855-877    _claude_chat_sync_metered
  9166-9173   _client_ip
 20363-20390  _clip_prune
 20393-20403  _clip_recfile_for
 20813-20819  _clip_should_velocity
 20444-20526  _clip_to_discord
  3404-3413   _close_ai_session
 21343-21358  _cohost_broadcast
 21328-21329  _cohost_cfg
 21384-21396  _cohost_fire_highlight
 21332-21340  _cohost_gate
 21361-21381  _cohost_highlight
  9626-9628   _conv_messages
  6486-6547   _cookie_alarm_loop
  2009-2014   _cookie_autofetch_info
  1992-1996   _cookie_autorefresh_info
  1895-1899   _cookie_header
  2026-2059   _cookies_selbst_holen
  3739-3751   _create_index_safe
 19288-19394  _crowdsec_status
 19234-19285  _crowdsec_via_lapi
 19138-19156  _cscli_bin
 19165-19178  _cscli_path
  6376-6401   _daily_summary_loop
 19196-19213  _darf_journal_lesen
 19789-19812  _db_maintenance_loop
  6345-6373   _db_vacuum_loop
 14976-15000  _detect_foreign_ad
  1540-1551   _diag_path_owner
 16237-16281  _director_finalize
 17178-17185  _director_for
 16186-16234  _director_mark
 20678-20681  _disc_state_get
 20684-20691  _disc_state_set
 19717-19726  _discord_bot_starten
 19681-19692  _discord_einladung_merken
 19729-19733  _discord_invite
 19695-19714  _discord_kontext
 20639-20675  _discord_live_thread
 16388-16400  _discord_notify
 19653-19678  _discord_ops_alert
 20537-20635  _discord_post_user
 20282-20288  _discord_stop
  6404-6481   _disk_alarm_loop
 22797-22846  _disk_autoclean
 22849-22862  _disk_guard_loop
 12894-12901  _drossel_hoeher
 12890-12891  _drossel_stufe
 12904-12912  _drossel_zuruecksetzen
 11271-11273  _dump_all_threads
  9904-9967   _enrich_proxies_with_geo
  2088-2149   _ensure_cookie_file_netscape
  8263-8266   _ensure_notify_topic
 10148-10185  _ensure_proxy_ready
  8217-8244   _ensure_topic
   704-706    _env_int
   709-711    _env_int_range
 16433-16446  _event_webhook
 11944-11957  _evolution_loop
  5529-5563   _extract_file_payload
  2221-2223   _extract_urls_from_streamurl_node
 19181-19188  _f2b_sudo_hint
  4373-4383   _fehler_text
  9805-9823   _fetch_proxy_list
 16965-16993  _fetch_tiktok_room_id
   787-790    _ff_cmd
 12723-12728  _find_chromium
  3128-3130   _find_external_recorder
  2226-2228   _find_stream_urls
 11644-11669  _fire_webhooks
  7313-7322   _fork_safe
   888-901    _freeai_chat_sync_metered
 19227-19231  _geo_lookup_ips
  3392-3401   _get_ai_session
  7146-7186   _get_live_info
  2842-2849   _get_resolve_semaphore
  7546-7918   _handle_single_tracking
 22619-22621  _hb
 22624-22641  _hb_while
 12200-12202  _highlight_cfg
 12205-12234  _highlight_observe
 12731-12749  _htmlov_screenshot_cmd
 16692-16702  _httpx_proxy
 11677-11689  _in_quiet_hours
 23230-23241  _init_db_oder_abbruch
 23812-23843  _install_fast_eventloop
  9032-9086   _install_fast_json
 11276-11292  _install_faulthandler
 17906-17915  _intel_ensure_schema
 17953-17988  _intel_index_loop
 17927-17937  _intel_index_one
 17918-17924  _intel_semantic
  4898-4907   _is_authorized
  7447-7453   _is_dead
  2211-2213   _is_hevc
 19216-19218  _is_private_ip
  1704-1711   _is_process_running
  6117-6124   _is_quiet_hours
  1333-1342   _is_upload_window
  4238-4253   _iso
  9121-9134   _json_error_handler
  6339-6340   _kick_broadcaster_id
  6251-6293   _kick_follower_count
  6235-6238   _kick_slug
 10756-10763  _kick_user_token
 23218-23227  _kickmod_boot
  3828-3831   _kind_from_filename
 11706-11708  _latest_popularity
 17574-17623  _live_react_loop
 17251-17563  _live_react_worker
 15836-15847  _live_transcript_push
 17565-17572  _live_users
 16284-16328  _living_title_loop
 19955-20027  _local_backup_scan
  9103-9117   _log_5xx
   777-784    _log_sicher
 13288-13300  _looks_like_codec_err
 13283-13285  _looks_like_source_expired
  7363-7393   _loop_fehler
 11296-11305  _loop_heartbeat
 22589-22616  _loop_lag_monitor
 11308-11376  _loop_watchdog_thread
 15716-15730  _loyalty_add
 15707-15713  _loyalty_get
 15733-15741  _loyalty_top
 11816-11818  _manual_donations_total
  4580-4599   _manual_status
  7455-7456   _mark_dead
 10424-10440  _marketing_loop
 21244-21262  _maybe_handle_command
 22948-22972  _maybe_hype_clip
 20332-20360  _meme_klassifizieren
  3706-3729   _migrate_columns
 21523-21534  _mod_is_exempt
 21537-21542  _mod_warn_first
 21545-21548  _mod_warn_text
 11984-11992  _modlog
  1033-1035   _multistream_targets
  7325-7326   _nc_create_subprocess_exec
  7329-7330   _nc_create_subprocess_shell
 10693-10710  _news_loop
 12011-12013  _normalize_ingest
  2441-2458   _note_check_duration
  8257-8260   _notify_topic_name
 15862-15870  _oracle_memories
 16135-16169  _oracle_memorize
 15873-15886  _oracle_persona
 15855-15859  _oracle_recent_text
 12357-12358  _ov_atomic_write
 12348-12350  _ov_bar
 14879-14891  _ov_clip_text
 12353-12354  _ov_oneline
 18893-18922  _overlay_push
 12677-12720  _overlay_render_size
 12080-12084  _overlay_session_reset
 18858-18860  _overlay_src_ok
 14963-14973  _own_invites
 12672-12674  _parse_size
 19402-19482  _parse_ssh_attacks
  6748-6781   _pause_resume_cmd
  1946-1990   _persist_refreshed_cookies
  1849-1881   _pick_checked_pull_proxy
  9202-9215   _pin_auth_value
  9261-9262   _pin_clear_fail
  9241-9244   _pin_locked
  9247-9258   _pin_note_fail
  9218-9238   _pin_ok
 18702-18727  _piper_pick_model
 18787-18836  _piper_say
 11606-11641  _post_json_threaded
 12651-12669  _probe_video_size
  1732-1749   _proc_is_recorder
 10117-10145  _proxy_pool_refresh_loop
  1815-1846   _proxy_report_recording
 11261-11263  _prune_stall_dumps
 10494-10615  _public_stats
  2017-2023   _pull_proxy_still
 16404-16430  _push_notify
  9421-9423   _pwa_dir
  9874-9889   _quick_validate_proxy
 11672-11674  _quiet_hours_config
  9386-9419   _rate_guard
 15677-15683  _react_warn
  7233-7272   _reap_proc
  8487-8554   _rec_auto_abschalten
  8434-8484   _rec_frueh_getrennt
  8321-8379   _rec_kategorie_melden
  8382-8431   _rec_totstreak_fortschreiben
  2481-2503   _record_check_outcome
   772-774    _redact_stream_urls
 10044-10114  _refresh_proxy_pool
  2258-2349   _resolve_via_html
  2622-2819   _resolve_via_webcast_api_v2
  2882-2949   _resolve_via_ytdlp
 20853-20982  _resolve_youtube_ingest
  2237-2255   _resolver_stumm
 12063-12074  _restream_active_sources
 13000-13124  _restream_avatar_feeder_start
 13127-13136  _restream_avatar_feeder_stop
 17024-17142  _restream_chat_guardian
 12237-12309  _restream_chat_push
 12334-12343  _restream_chat_push_async
 12752-12861  _restream_html_overlay_start
 12864-12877  _restream_html_overlay_stop
 12022-12045  _restream_overlay_files
 17627-17659  _restream_platform_state
 17822-17857  _restream_resume_after_restart
 13184-13242  _restream_tts_enqueue_wav
 12613-12645  _restream_tts_feeder
 12610-12611  _restream_tts_fifo_path
 13139-13166  _restream_tts_start
 13168-13182  _restream_tts_stop
 17665-17819  _restream_verify_loop
 19920-19932  _retention_loop
 19914-19917  _retention_scan
  2579-2581   _room_is_abo
  5567-5684   _run_ai_call
 11399-11412  _run_async_from_flask
 19221-19224  _run_priv
 23800-23808  _run_selfcheck_and_exit
 19935-19946  _s3_client
  7482-7533   _safe_send
  4506-4522   _sample_net_throughput
  2533-2554   _schedule_next_check
 19868-19911  _scheduler_loop
  3732-3736   _schema_pk
 11416-11421  _scraper_session
 21551-21590  _screen_full
 10807-10844  _sec_headers
  2216-2218   _select_stream_from_data_section
 23578-23797  _selfcheck
  8269-8303   _send_live_notice
  1356-1360   _should_defer_upload
 20406-20441  _shrink_for_discord
  9426-9438   _sicheres_ziel
 19748-19786  _sicherheits_erinnerung_loop
 22869-22886  _sign_health_check
 22889-22908  _sign_health_loop
  4256-4281   _sitzung_bestimmen
  7342-7353   _spawn
 24218-24248  _spawn_from_flask
 16704-16962  _start_chat_listener
 11379-11396  _start_loop_watchdog
 10642-10688  _stats_loop
 10621-10624  _stats_output_path
 10627-10639  _stats_write
 18739-18753  _stimme_saubern
 18760-18784  _stimme_schon_gesagt
  7997-8013   _storage_cleanup_loop
 22928-22935  _story_for
  3153-3159   _stream_url_expiry
  3161-3166   _stream_url_ttl
 14926-14933  _streamer_persona_get
 20052-20174  _system_backup
 20183-20213  _system_backup_loop
 11221-11239  _task_auf_bot_schleife
  9826-9865   _test_proxy
 10372-10388  _testpush_resolve_live
  7458-7479   _tg_sprache_setzen
  8176-8186   _tg_topics_load_into_mem
  8173-8174   _tg_topics_path
  8188-8195   _tg_topics_save
  9176-9184   _token_ok
  8198-8202   _topic_forget
 11692-11703  _tracking_max_duration
  4036-4050   _tracking_remove_cleanup
  4067-4079   _tracking_resume_cleanup
  1598-1621   _try_attach_file_handler
 18729-18737  _tts_cleanup
 10348-10352  _tunnel_effective
 18225-18278  _twitch_channel_status
 21593-21738  _twitch_chat_loop
 20697-20710  _twitch_clip_versuchen
 21407-21510  _twitch_eventsub_loop
  1379-1392   _upload_queue_add
  1403-1405   _upload_queue_count
  1362-1371   _upload_queue_load
  1352-1354   _upload_queue_path
  1394-1401   _upload_queue_remove
  1373-1377   _upload_queue_save
  1407-1448   _upload_window_loop
  7206-7213   _uptime_s
 11999-12008  _url_host
   848-852    _usage_record_claude
 23042-23064  _v37_pause_source
 23006-23016  _v37_restream_restart
 23019-23039  _v37_unpause_source
  7396-7440   _verbindung_verloren
  6296-6327   _viewer_sample_loop
  9265-9268   _wants_html
  7216-7230   _warn_empty_env
 22662-22783  _watchdog_loop
 21128-21136  _wchat_thank_ok
 16472-16502  _whisper_get_model
  7303-7310   _whisper_native_section
 15664-15670  _whisper_pool
 16596-16628  _whisper_segments
 16504-16520  _whisper_stumm
 16523-16593  _whisper_transcribe
 12405-12567  _write_restream_overlay
 12367-12402  _write_restream_overlay_async
 21762-21858  _youtube_api_chat_loop
 18281-18384  _youtube_api_status
 18387-18454  _youtube_channel_status
 21861-22022  _youtube_chat_loop
 20713-20738  _youtube_clip_versuchen
 20988-21001  _youtube_restream_autoconfig
 21004-21028  _youtube_restream_autoconfig_inner
 21095-21123  _youtube_send
 18522-18563  _youtube_set_channel
 21031-21065  _yt_access_token
 21068-21083  _yt_live_chat_id
 21091-21092  _yt_sendrate_cfg
 21741-21756  _yt_timeout
  2866-2867   _ytdlp_detect_available
  2869-2880   _ytdlp_note_result
 11266-11268  _zombie_child_count
  7082-7106   about
  3947-3951   add_ai_log_entry
  3864-3867   add_archive_entry
  4544-4546   add_archive_rule
  4284-4355   add_recording
  4011-4028   add_tracking
  5687-5720   ai
  3537-3610   ai_chat
  3644-3654   ai_history_append
  3656-3661   ai_history_clear
  3633-3642   ai_history_load
  3618-3631   ai_rate_limit_check
  5749-5757   aireset
 16003-16022  azrael_chat
 22027-22149  brain_cmd
  3169-3174   build_recording_cmd
  4031-4034   bulk_add_trackings
  6550-6609   bulkadd
  8016-8156   check_all_trackings
  4083-4095   claim_live_transition
 15003-15596  class KickModerator
 13303-14766  class RestreamManager
 10231-10273  classify_proxy_anonymity
  5795-5993   cleanup
  4834-4840   cleanup_old_recordings
  4229-4236   clear_recording
 20741-20810  clip_moment
  4496-4499   compute_storage_forecast
  6672-6745   cookies_cmd
  4002-4008   count_trackings_for_chat
  3934-3945   decide_preferred_recorder
  3874-3877   delete_archive_entry
  4548-4550   delete_archive_rule
  5224-5371   diag
 22261-22322  einnahmen_cmd
  4490-4493   find_recordings_by_fingerprint
  3895-3911   finish_recording_attempt
  4055-4057   get_all_active_trackings
  3962-3964   get_all_checks
  4357-4360   get_all_recordings
  4439-4441   get_all_tags_with_counts
  4467-4470   get_annotations_for_recording
  3869-3872   get_archive_entry
  4460-4463   get_bookmarked_recordings
  2076-2081   get_cookie_health
  4427-4433   get_event_log
  3918-3932   get_last_recording_attempt
  2952-3090   get_live_status
  4773-4776   get_manual_recordings
  4475-4478   get_or_compute_inspect_sync
  4875-4878   get_outcome_breakdown
  4446-4449   get_priority_poll_interval
  3913-3916   get_recent_recording_attempts
  4362-4365   get_recording_by_id
  4453-4456   get_recording_note
  3338-3361   get_redis
  3991-3994   get_stats
  4828-4832   get_storage_stats
  4568-4570   get_tiktok_status_distribution
  4097-4106   get_tracking_state
  4052-4053   get_trackings_for_group
  4789-4792   get_trash_recordings
  8557-9011   handle_recording_finished
  3759-3819   init_db
  4540-4542   list_archive_rules
  5028-5066   live
  7536-7544   live_check_worker
  3416-3450   llm_chat
  3473-3501   llm_chat_sync
  3458-3470   llm_list_models
  4386-4419   log_event
  1666-1699   log_recording_failure
  6895-6944   logs_cmd
 23269-23568  main
  5723-5746   on_ai_media
  7021-7047   on_ai_reply
  7050-7079   on_azrael_mention
  7111-7141   on_callback
 16028-16132  oracle_handle
  6784-6787   pause_tracking
  4888-4893   profile_keyboard
  6846-6892   quota
  7920-7994   reaper_loop
  4564-4566   record_tiktok_status
  5762-5792   recstatus
  3363-3371   redis_get_json
  3374-3380   redis_set_json
 22325-22335  report_cmd
 10276-10278  report_proxy_result
  2352-2394   resolve_tiktok_live_stream
  4784-4787   restore_recording
  6790-6793   resume_tracking
  4553-4558   run_archive_rules
 22338-22569  run_bot
 11123-11212  run_flask
  4528-4531   sample_bandwidth_for_active
  3954-3960   save_tiktok_check
  4221-4227   set_recording_file
  4060-4064   set_tracking_paused
  4779-4782   soft_delete_recording
  8309-8319   split_and_send_video
  4941-4983   start
  3879-3893   start_recording_attempt
  5996-6034   stats
  4718-4771   stop_manual_recording
  6796-6843   stoprec
  6220-6228   summary_cmd
  6947-7018   sysres
  5373-5517   teststream
  4985-5026   tiktok
  6612-6669   topusers
  5103-5160   track
  5068-5100   track_exact
  5174-5222   tracklist
  4602-4716   trigger_manual_recording
  4182-4219   try_acquire_recording_lock
  4795-4797   universal_search
  5162-5172   untrack
 22152-22258  update_cmd
  4485-4488   update_recording_fingerprint
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
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
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
ffmpeg_filters.py      avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livefolge.py           braucht_url_nachschlag, hat_stream_url, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
schemastand.py         lege_an, lies, pruefe, schreibe, streng
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
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, threads, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
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
